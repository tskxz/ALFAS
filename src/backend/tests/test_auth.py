import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from flask import Flask
from werkzeug.security import generate_password_hash

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api.auth.login import auth_bp
from db import db
from models import Role, RoleUser, User, Userstate

    
class FakeSession:
    def __init__(self, roles=()):
        self.roles = roles

    def get(self, model, identity):
        return SimpleNamespace(state="Ativo")

    def query(self, column):
        query = Mock()
        query.join.return_value = query
        query.filter.return_value = query
        query.order_by.return_value = query
        query.all.return_value = [(role,) for role in self.roles]
        return query


def user_query(user):
    query = Mock()
    query.filter.return_value.first.return_value = user
    return query


class AuthEndpointTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite://",
            JWT_SECRET_KEY="test-jwt-secret-that-is-at-least-32-bytes",
        )
        db.init_app(self.app)
        self.app.register_blueprint(auth_bp, url_prefix="/api/auth")
        self.client = self.app.test_client()
        self.user = SimpleNamespace(
            id=42,
            email="user@example.pt",
            password=generate_password_hash("Password1"),
            userstate_id=1,
        )

    def test_login_returns_signed_token_with_user_and_role(self):
        with self.app.app_context(), patch.object(User, "query", user_query(self.user)), patch.object(
            db, "session", FakeSession(("Registado",))
        ):
            response = self.client.post(
                "/api/auth/login",
                json={"email": "USER@example.pt", "password": "Password1"},
            )

        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertEqual(body["user"], {"id": 42, "role": "Registado", "roles": ["Registado"]})
        protected = self.client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {body['access_token']}"},
        )
        self.assertEqual(protected.status_code, 200)
        self.assertEqual(protected.get_json()["user_id"], 42)

    def test_invalid_password_returns_401(self):
        with self.app.app_context(), patch.object(User, "query", user_query(self.user)):
            response = self.client.post(
                "/api/auth/login",
                json={"email": "user@example.pt", "password": "incorrect"},
            )

        self.assertEqual(response.status_code, 401)

    def test_private_route_requires_valid_token(self):
        response = self.client.get("/api/auth/me")
        self.assertEqual(response.status_code, 401)

        response = self.client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid-token"},
        )
        self.assertEqual(response.status_code, 401)

    def test_invalid_request_returns_400(self):
        response = self.client.post("/api/auth/login", json={"email": "user@example.pt"})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
