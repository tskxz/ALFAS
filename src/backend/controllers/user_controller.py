from models.user import User
from db import db


class UserController:

    @classmethod
    def create_user(cls, user_data: dict) -> User:
        """
        Cria e persiste um novo utilizador na base de dados.
        Aplica hash à palavra-passe caso esteja em texto simples.
        """
        user = User.from_dict(user_data)
        plain_password = user_data.get("password")
        if plain_password and not plain_password.startswith(("scrypt:", "pbkdf2:")):
            user.set_password(plain_password)

        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_user_by_id(cls, user_id: int) -> User | None:
        """
        Procura um utilizador pelo ID.
        """
        return db.session.get(User, user_id)

    @classmethod
    def get_user_by_email(cls, email: str) -> User | None:
        """
        Procura um utilizador pelo e-mail.
        """
        return User.query.filter_by(email=email).first()

    @classmethod
    def get_all_users(cls, limit: int = 100, offset: int = 0) -> list[User]:
        """
        Retorna uma lista paginada de utilizadores.
        """
        return User.query.limit(limit).offset(offset).all()

    @classmethod
    def update_user(cls, user_id: int, update_data: dict) -> User | None:
        """
        Atualiza campos específicos de um utilizador existente pelo ID.
        """
        user = cls.get_user_by_id(user_id)
        if not user:
            return None

        for field, value in update_data.items():
            if field == "password":
                user.set_password(value)
            elif hasattr(user, field) and field != "id":
                setattr(user, field, value)

        db.session.commit()
        return user

    @classmethod
    def delete_user(cls, user_id: int) -> bool:
        """
        Remove um utilizador da base de dados.
        """
        user = cls.get_user_by_id(user_id)
        if not user:
            return False

        db.session.delete(user)
        db.session.commit()
        return True

