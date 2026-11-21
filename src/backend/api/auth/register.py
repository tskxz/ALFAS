import re
from datetime import date

from flask import Blueprint, current_app, jsonify, request
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from db import db
from models import Gender, Role, RoleUser, Schoolyear, User, Userstate

register_bp = Blueprint('register', __name__)


def _is_valid_email(email):
    return len(email) <= 255 and re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email)


@register_bp.post("/register")
@register_bp.post("/auth/register")
def register():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "O pedido tem de conter um objeto JSON válido."}), 400

    required_fields = ("name", "email", "birth_date", "schoolyear", "gender", "password")
    if any(
        not isinstance(data.get(field), str) or not data[field].strip()
        for field in required_fields
    ):
        return jsonify({"error": "Preencha todos os campos obrigatórios."}), 400

    name = str(data["name"]).strip()
    email = str(data["email"]).strip().lower()
    password = str(data["password"])
    if len(name) < 2 or len(name) > 255:
        return jsonify({"error": "O nome deve ter entre 2 e 255 caracteres."}), 400
    if not _is_valid_email(email):
        return jsonify({"error": "Indique um endereço de email válido com até 255 caracteres."}), 400
    if len(password) < 8 or not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        return jsonify({"error": "A palavra-passe deve ter pelo menos 8 caracteres, uma letra e um número."}), 400

    birth_date_value = data["birth_date"].strip()
    try:
        birth_date = date.fromisoformat(birth_date_value)
    except (TypeError, ValueError):
        return jsonify({"error": "Indique uma data de nascimento válida no formato AAAA-MM-DD."}), 400
    if birth_date.isoformat() != birth_date_value:
        return jsonify({"error": "Indique uma data de nascimento válida no formato AAAA-MM-DD."}), 400

    schoolyear_value = str(data["schoolyear"]).strip()
    course_name_value = data.get("course_name")
    if course_name_value is not None and not isinstance(course_name_value, str):
        return jsonify({"error": "O nome do curso tem de ser texto."}), 400
    course_name = (course_name_value or "").strip()
    schoolyear_options = {f"{year}.\u00ba ano" for year in range(1, 13)}
    course_types = {
        "licenciatura": "Licenciatura",
        "mestrado": "Mestrado",
        "ctesp": "CTeSP",
    }

    if schoolyear_value.lower() in course_types:
        schoolyear_value = course_types[schoolyear_value.lower()]
        if not course_name or len(course_name) > 255:
            return jsonify({"error": "Indique o nome do curso (até 255 caracteres)."}), 400
    elif schoolyear_value not in schoolyear_options:
        return jsonify({"error": "Selecione um ano de escolaridade ou tipo de curso válido."}), 400
    else:
        course_name = None

    gender_options = {
        "feminino": "Feminino",
        "masculino": "Masculino",
        "outro": "Outro",
    }
    gender_name = gender_options.get(str(data["gender"]).strip().lower())
    if not gender_name:
        return jsonify({"error": "Selecione uma das opções de género disponíveis."}), 400

    if birth_date >= date.today():
        return jsonify({"error": "A data de nascimento tem de ser anterior à data de hoje."}), 400

    today = date.today()
    age = today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )
    is_minor = age < 18

    guardian_name_value = data.get("guardian_name")
    guardian_email_value = data.get("guardian_email")
    if guardian_name_value is not None and not isinstance(guardian_name_value, str):
        return jsonify({"error": "O nome do encarregado de educação tem de ser texto."}), 400
    if guardian_email_value is not None and not isinstance(guardian_email_value, str):
        return jsonify({"error": "O email do encarregado de educação tem de ser texto."}), 400
    guardian_name = (guardian_name_value or "").strip()
    guardian_email = (guardian_email_value or "").strip().lower()
    parental_consent = data.get("parental_consent") is True

    if is_minor:
        if not guardian_name or len(guardian_name) > 255:
            return jsonify({"error": "Indique o nome do encarregado de educação (até 255 caracteres)."}), 400
        if not _is_valid_email(guardian_email):
            return jsonify({"error": "Indique um email válido para o encarregado de educação."}), 400
        if not parental_consent:
            return jsonify({"error": "É necessário o consentimento do encarregado de educação."}), 400
    else:
        guardian_name = None
        guardian_email = None
        parental_consent = False

    try:
        if User.query.filter(db.func.lower(User.email) == email).first():
            return jsonify({"error": "Este email já está registado."}), 409

        schoolyear = Schoolyear.query.filter(
            db.func.lower(Schoolyear.schoolyear) == schoolyear_value.lower()
        ).first()
        gender = Gender.query.filter(
            db.func.lower(Gender.gender) == gender_name.lower()
        ).first()
        state_name = "pendente" if is_minor else "ativo"
        user_state = Userstate.query.filter(
            db.func.lower(Userstate.state) == state_name
        ).first()
        user_role = Role.query.filter(
            db.func.lower(Role.name).in_(["registado", "utilizador registado", "user"])
        ).first()

        if not user_state:
            user_state = Userstate(state=state_name.capitalize())
            db.session.add(user_state)
            db.session.flush()

        if not user_role:
            user_role = Role(name="Registado")
            db.session.add(user_role)
            db.session.flush()

        if not schoolyear:
            schoolyear = Schoolyear(schoolyear=schoolyear_value)
            db.session.add(schoolyear)
            db.session.flush()

        if not gender:
            gender = Gender(gender=gender_name)
            db.session.add(gender)
            db.session.flush()

        user = User(
            name=name,
            email=email,
            birth_date=birth_date,
            schoolyear_id=schoolyear.id,
            course_name=course_name,
            gender_id=gender.id,
            userstate_id=user_state.id,
            parental_consent=parental_consent,
            guardian_name=guardian_name,
            guardian_email=guardian_email,
            password=generate_password_hash(password, method="scrypt"),
        )
        db.session.add(user)
        db.session.flush()
        db.session.add(RoleUser(user_id=user.id, role_id=user_role.id))
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        try:
            if User.query.filter(db.func.lower(User.email) == email).first():
                return jsonify({"error": "Este email já está registado."}), 409
        except Exception:
            current_app.logger.exception("Erro ao verificar conflito de email no registo.")
        current_app.logger.exception("Erro de integridade ao criar a conta de utilizador.")
        return jsonify({"error": "Não foi possível concluir o registo. Tente novamente."}), 500
    except Exception:
        db.session.rollback()
        current_app.logger.exception("Erro ao criar a conta de utilizador.")
        return jsonify({"error": "Não foi possível concluir o registo. Tente novamente."}), 500

    message = (
        "Pedido de registo recebido. A conta ficará pendente de validação do consentimento parental."
        if is_minor
        else "Registo concluído com sucesso."
    )
    return jsonify({"message": message}), 201


