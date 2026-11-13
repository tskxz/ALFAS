import re
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash

try:
    from db.connect import get_db_connection
except ImportError:
    from ..db.connect import get_db_connection


class User:
    TABLE_NAME = "users"

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
    ):
        self.id = id
        self.name = name
        self.gender_id = int(gender_id)
        self.schoolyear_id = int(schoolyear_id)
        self.birth_date = self._parse_date(birth_date)
        self.parental_consent = bool(parental_consent)
        self.email = email
        self.img_url = img_url
        self.email_verified_at = self._parse_datetime(email_verified_at)
        self.password = password
        self.remember_token = remember_token
        self.userstate_id = int(userstate_id)

    
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
        """
        Calcula a idade atual com base no birth_date.
        """
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
        """
        Retorna True se o utilizador for menor de idade (< 18 anos).
        """
        return self.age < 18

    def can_activate(self) -> bool:
        """
        Se a idade for inferior a 18 anos, parental_consent tem de ser True (1)
        para a conta poder ser ativada.
        """
        if self.is_minor and not self.parental_consent:
            return False
        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validação de sintaxe de e-mail.
        """
        regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.match(regex, email))


    def set_password(self, plain_password: str) -> None:
        """
        Gera hash seguro da palavra-passe.
        """
        self.password = generate_password_hash(plain_password)

    def check_password(self, plain_password: str) -> bool:
        """
        Verifica a palavra-passe fornecida contra o hash armazenado.
        """
        if not self.password:
            return False
        return check_password_hash(self.password, plain_password)

    
    def to_dict(self, include_sensitive: bool = False) -> dict:
        """
        Serializa o objeto para dicionário para ter respostas json.
        """
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
    def from_dict(cls, data: dict):
        """
        Cria uma instância de User a partir de um dicionário.
        """
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


    @classmethod
    def create_table_sql(cls) -> str:
        return """
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            gender_id INT UNSIGNED NOT NULL,
            schoolyear_id INT UNSIGNED NOT NULL,
            birth_date DATE NOT NULL,
            parental_consent BOOLEAN NOT NULL DEFAULT 0,
            email VARCHAR(255) NOT NULL UNIQUE,
            img_url VARCHAR(500) NULL DEFAULT NULL,
            email_verified_at TIMESTAMP NULL DEFAULT NULL,
            password VARCHAR(255) NOT NULL,
            remember_token VARCHAR(100) NULL DEFAULT NULL,
            userstate_id INT UNSIGNED NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """

    # TODO: MOVER ISTO PARA OUTRO FICHEIRO
    
    @classmethod
    def create_table(cls, cnx=None) -> None:
        """
        Executa a criação da tabela `users` na base de dados conectada.
        """
        close_cnx = False
        if cnx is None:
            cnx = get_db_connection(with_db=True)
            close_cnx = True
        try:
            cursor = cnx.cursor()
            cursor.execute(cls.create_table_sql())
            cnx.commit()
            cursor.close()
        finally:
            if close_cnx:
                cnx.close()

    @classmethod
    def find_by_id(cls, user_id: int, cnx=None):
        """
        Procura um utilizador pelo seu ID.
        """
        close_cnx = False
        if cnx is None:
            cnx = get_db_connection(with_db=True)
            close_cnx = True
        try:
            cursor = cnx.cursor(dictionary=True)
            query = f"SELECT * FROM {cls.TABLE_NAME} WHERE id = %s LIMIT 1"
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            cursor.close()
            return cls.from_dict(row) if row else None
        finally:
            if close_cnx:
                cnx.close()

    @classmethod
    def find_by_email(cls, email: str, cnx=None):
        """
        Procura um utilizador pelo seu endereço de e-mail.
        """
        close_cnx = False
        if cnx is None:
            cnx = get_db_connection(with_db=True)
            close_cnx = True
        try:
            cursor = cnx.cursor(dictionary=True)
            query = f"SELECT * FROM {cls.TABLE_NAME} WHERE email = %s LIMIT 1"
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            cursor.close()
            return cls.from_dict(row) if row else None
        finally:
            if close_cnx:
                cnx.close()

    @classmethod
    def all(cls, limit: int = 100, offset: int = 0, cnx=None) -> list:
        """
        Retorna a lista de utilizadores com paginação.
        """
        close_cnx = False
        if cnx is None:
            cnx = get_db_connection(with_db=True)
            close_cnx = True
        try:
            cursor = cnx.cursor(dictionary=True)
            query = f"SELECT * FROM {cls.TABLE_NAME} LIMIT %s OFFSET %s"
            cursor.execute(query, (limit, offset))
            rows = cursor.fetchall()
            cursor.close()
            return [cls.from_dict(r) for r in rows]
        finally:
            if close_cnx:
                cnx.close()

    def save(self, cnx=None) -> "User":
        """
        Insere ou atualiza o registo do utilizador na base de dados MySQL.
        """
        close_cnx = False
        if cnx is None:
            cnx = get_db_connection(with_db=True)
            close_cnx = True
        try:
            cursor = cnx.cursor()
            if self.id is None:
                query = f"""
                INSERT INTO {self.TABLE_NAME} (
                    name, gender_id, schoolyear_id, birth_date,
                    parental_consent, email, img_url, email_verified_at,
                    password, remember_token, userstate_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    self.name,
                    self.gender_id,
                    self.schoolyear_id,
                    self.birth_date,
                    1 if self.parental_consent else 0,
                    self.email,
                    self.img_url,
                    self.email_verified_at,
                    self.password,
                    self.remember_token,
                    self.userstate_id,
                )
                cursor.execute(query, values)
                self.id = cursor.lastrowid
            else:
                query = f"""
                UPDATE {self.TABLE_NAME} SET
                    name = %s,
                    gender_id = %s,
                    schoolyear_id = %s,
                    birth_date = %s,
                    parental_consent = %s,
                    email = %s,
                    img_url = %s,
                    email_verified_at = %s,
                    password = %s,
                    remember_token = %s,
                    userstate_id = %s
                WHERE id = %s
                """
                values = (
                    self.name,
                    self.gender_id,
                    self.schoolyear_id,
                    self.birth_date,
                    1 if self.parental_consent else 0,
                    self.email,
                    self.img_url,
                    self.email_verified_at,
                    self.password,
                    self.remember_token,
                    self.userstate_id,
                    self.id,
                )
                cursor.execute(query, values)
            cnx.commit()
            cursor.close()
            return self
        finally:
            if close_cnx:
                cnx.close()

    def delete(self, cnx=None) -> bool:
        """
        Remove o utilizador da base de dados.
        """
        if self.id is None:
            return False
        close_cnx = False
        if cnx is None:
            cnx = get_db_connection(with_db=True)
            close_cnx = True
        try:
            cursor = cnx.cursor()
            query = f"DELETE FROM {self.TABLE_NAME} WHERE id = %s"
            cursor.execute(query, (self.id,))
            cnx.commit()
            deleted = cursor.rowcount > 0
            cursor.close()
            return deleted
        finally:
            if close_cnx:
                cnx.close()

