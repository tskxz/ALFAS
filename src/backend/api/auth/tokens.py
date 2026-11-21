from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app


ACCESS_TOKEN_TTL_SECONDS = 3600


def _jwt_secret():
    secret = current_app.config.get("JWT_SECRET_KEY")
    if not isinstance(secret, str) or len(secret.encode("utf-8")) < 32:
        raise RuntimeError("JWT_SECRET_KEY must be configured with at least 32 bytes.")
    return secret


def create_access_token(user_id, roles):
    now = datetime.now(timezone.utc)
    role_names = sorted(set(roles))
    payload = {
        "sub": str(user_id),
        "user_id": user_id,
        "role": role_names[0],
        "roles": role_names,
        "iat": now,
        "exp": now + timedelta(seconds=ACCESS_TOKEN_TTL_SECONDS),
    }
    return jwt.encode(payload, _jwt_secret(), algorithm="HS256")


def decode_access_token(token):
    return jwt.decode(
        token,
        _jwt_secret(),
        algorithms=["HS256"],
        options={"require": ["sub", "user_id", "role", "roles", "iat", "exp"]},
    )
