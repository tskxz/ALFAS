from flask import Blueprint, current_app, g, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash

from api.auth.authorization import token_required
from api.auth.tokens import ACCESS_TOKEN_TTL_SECONDS, create_access_token
from db import db
from models import Role, RoleUser, User, Userstate


auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "O pedido tem de conter um objeto JSON válido."}), 400

    email = data.get("email")
    password = data.get("password")
    if (
        not isinstance(email, str)
        or not email.strip()
        or not isinstance(password, str)
        or not password
    ):
        return jsonify({"error": "Indique o email e a palavra-passe."}), 400

    try:
        user = User.query.filter(db.func.lower(User.email) == email.strip().lower()).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({"error": "Email ou palavra-passe inválidos."}), 401

        user_state = db.session.get(Userstate, user.userstate_id)
        if not user_state or user_state.state.strip().lower() != "ativo":
            return jsonify({"error": "Email ou palavra-passe inválidos."}), 401

        roles = [
            row[0]
            for row in (
                db.session.query(Role.name)
                .join(RoleUser, Role.id == RoleUser.role_id)
                .filter(RoleUser.user_id == user.id)
                .order_by(Role.name)
                .all()
            )
        ]
        if not roles:
            return jsonify({"error": "Email ou palavra-passe inválidos."}), 401

        access_token = create_access_token(user.id, roles)
    except RuntimeError:
        current_app.logger.exception("A chave JWT não está configurada corretamente.")
        return jsonify({"error": "A autenticação não está configurada."}), 500
    except SQLAlchemyError:
        current_app.logger.exception("Erro ao autenticar o utilizador.")
        return jsonify({"error": "Não foi possível concluir a autenticação."}), 500

    return jsonify(
        {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": ACCESS_TOKEN_TTL_SECONDS,
            "user": {
                "id": user.id,
                "role": roles[0],
                "roles": roles,
            },
        }
    ), 200


@auth_bp.get("/me")
@token_required
def current_session():
    return jsonify(
        {
            "user_id": g.authenticated_user_id,
            "role": g.authenticated_role,
            "roles": g.authenticated_roles,
        }
    ), 200
