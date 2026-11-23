from functools import wraps

import jwt
from flask import current_app, g, jsonify, request

from api.auth.tokens import decode_access_token


def token_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        authorization = request.headers.get("Authorization", "")
        scheme, separator, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not separator or not token:
            return jsonify({"error": "É necessário um token Bearer válido."}), 401

        try:
            claims = decode_access_token(token)
            user_id = claims.get("user_id")
            roles = claims.get("roles")
            if (
                not isinstance(user_id, int)
                or user_id <= 0
                or claims.get("sub") != str(user_id)
                or not isinstance(roles, list)
                or not roles
                or any(not isinstance(role, str) or not role for role in roles)
                or claims.get("role") not in roles
            ):
                raise jwt.InvalidTokenError("Invalid authentication claims.")
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido ou expirado."}), 401
        except RuntimeError:
            current_app.logger.exception("A chave JWT não está configurada corretamente.")
            return jsonify({"error": "A autenticação não está configurada."}), 500

        g.authenticated_user_id = user_id
        g.authenticated_role = claims["role"]
        g.authenticated_roles = roles
        return view(*args, **kwargs)

    return wrapped
