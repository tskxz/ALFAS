from datetime import date, datetime
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.mysql import BIGINT, INTEGER


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    gender_id = db.Column(INTEGER(unsigned=True), nullable=False)
    schoolyear_id = db.Column(INTEGER(unsigned=True), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    parental_consent = db.Column(db.Boolean, nullable=False, default=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    img_url = db.Column(db.String(500), nullable=True, default=None)
    email_verified_at = db.Column(db.TIMESTAMP, nullable=True, default=None)
    password = db.Column(db.String(255), nullable=False)
    remember_token = db.Column(db.String(100), nullable=True, default=None)
    userstate_id = db.Column(INTEGER(unsigned=True), nullable=False)

    def __init__(
        self,
        name: str,
        gender_id: int,
        schoolyear_id: int,
        birth_date,
        email: str,
        password: str,
        userstate_id: int,
        parental_consent: bool = False,
        img_url: str = None,
        email_verified_at=None,
        remember_token: str = None,
        id: int = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.id = id
        self.name = name
        self.gender_id = int(gender_id) if gender_id is not None else None
        self.schoolyear_id = int(schoolyear_id) if schoolyear_id is not None else None
        self.birth_date = self._parse_date(birth_date)
        self.parental_consent = bool(parental_consent)
        self.email = email
        self.img_url = img_url
        self.email_verified_at = self._parse_datetime(email_verified_at)
        self.password = password
        self.remember_token = remember_token
        self.userstate_id = int(userstate_id) if userstate_id is not None else None

    @staticmethod
    def _parse_date(value):
        if value is None or isinstance(value, date):
            return value
        if isinstance(value, str):
            return datetime.strptime(value.split("T")[0], "%Y-%m-%d").date()
        return value

    @staticmethod
    def _parse_datetime(value):
        if value is None or isinstance(value, datetime):
            return value
        if isinstance(value, str):
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
        return value

    @property
    def age(self) -> int:
        """Calcula a idade dinâmica com base no birth_date."""
        if not self.birth_date:
            return 0
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

    @property
    def is_minor(self) -> bool:
        """Verifica se o utilizador é menor de idade (< 18 anos)."""
        return self.age < 18

    def can_activate(self) -> bool:
        """
        Regra do Dicionário de Dados:
        Se a idade for inferior a 18 anos, parental_consent tem obrigatoriamente
        de ser True (1) para a conta poder ser ativada.
        """
        if self.is_minor and not self.parental_consent:
            return False
        return True

    def set_password(self, plain_password: str) -> None:
        """Gera hash seguro da palavra-passe."""
        self.password = generate_password_hash(plain_password)

    def check_password(self, plain_password: str) -> bool:
        """Compara a palavra-passe fornecida com o hash armazenado."""
        if not self.password:
            return False
        return check_password_hash(self.password, plain_password)

    def to_dict(self, include_sensitive: bool = False) -> dict:
        """Serializa o modelo para dicionário (respostas JSON)."""
        data = {
            "id": self.id,
            "name": self.name,
            "gender_id": self.gender_id,
            "schoolyear_id": self.schoolyear_id,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "age": self.age,
            "is_minor": self.is_minor,
            "parental_consent": self.parental_consent,
            "email": self.email,
            "img_url": self.img_url,
            "email_verified_at": (
                self.email_verified_at.isoformat() if self.email_verified_at else None
            ),
            "userstate_id": self.userstate_id,
        }
        if include_sensitive:
            data["password"] = self.password
            data["remember_token"] = self.remember_token
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Instancia um User a partir de um dicionário."""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            gender_id=data.get("gender_id"),
            schoolyear_id=data.get("schoolyear_id"),
            birth_date=data.get("birth_date"),
            parental_consent=data.get("parental_consent", False),
            email=data.get("email"),
            img_url=data.get("img_url"),
            email_verified_at=data.get("email_verified_at"),
            password=data.get("password"),
            remember_token=data.get("remember_token"),
            userstate_id=data.get("userstate_id"),
        )

    def __repr__(self):
        return f"<User id={self.id} email='{self.email}' name='{self.name}'>"
