import os
import re
from datetime import date

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate, upgrade
from dotenv import load_dotenv
import mysql.connector
from sqlalchemy.exc import IntegrityError
from db import db
from werkzeug.security import generate_password_hash

# Carrega os modelos para o Flask-Migrate reconhecer as tabelas.
from models import (
    Activity,
    Answer,
    Content,
    Contenttype,
    Gender,
    Healtharea,
    News,
    Qastate,
    Question,
    Quiz,
    QuizUser,
    Quiztype,
    Resource,
    Resourcelevel,
    ResourcelevelUser,
    ResourceUser,
    Resourcestate,
    Resourcetype,
    Role,
    RoleUser,
    Schoolyear,
    User,
    Userstate,
)

load_dotenv()

app = Flask(__name__)
CORS(app)


# TODO: Usar db/connect.py para respeitar o DRY

# config db for mysql
db_user = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
db_host = os.environ.get("DB_HOST", "127.0.0.1")
db_port = os.environ.get("DB_PORT", "3306")
db_database = os.environ.get("DB_DATABASE")


def ensure_database_exists():
    if not db_database:
        raise RuntimeError("DB_DATABASE must be set before starting the application.")

    connection = mysql.connector.connect(
        host=db_host,
        port=int(db_port),
        user=db_user,
        password=db_password,
    )
    try:
        database_name = db_database.replace("`", "``")
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{database_name}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
    finally:
        connection.close()


ensure_database_exists()

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
)

db.init_app(app)

migrate = Migrate(app, db)


@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello World!"})


@app.get("/api/schoolyears")
def get_schoolyears():
    schoolyears = Schoolyear.query.order_by(Schoolyear.id).all()
    return jsonify([
        {"id": schoolyear.id, "schoolyear": schoolyear.schoolyear}
        for schoolyear in schoolyears
    ])


@app.post("/api/register")
def register():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "O pedido tem de conter dados JSON válidos."}), 400

    required_fields = ("name", "email", "birth_date", "schoolyear", "gender", "password")
    if any(not data.get(field) for field in required_fields):
        return jsonify({"error": "Preencha todos os campos obrigatórios."}), 400

    name = str(data["name"]).strip()
    email = str(data["email"]).strip().lower()
    password = str(data["password"])
    if len(name) < 2 or len(name) > 255:
        return jsonify({"error": "O nome deve ter entre 2 e 255 caracteres."}), 400
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        return jsonify({"error": "Indique um endereço de email válido."}), 400
    if len(email) > 255:
        return jsonify({"error": "O endereço de email é demasiado longo."}), 400
    if len(password) < 8 or not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        return jsonify({"error": "A palavra-passe deve ter pelo menos 8 caracteres, uma letra e um número."}), 400

    try:
        birth_date = date.fromisoformat(str(data["birth_date"]))
    except (TypeError, ValueError):
        return jsonify({"error": "A data de nascimento ou as opções selecionadas são inválidas."}), 400

    schoolyear_value = str(data["schoolyear"]).strip()
    course_name = str(data.get("course_name") or "").strip()
    schoolyear_options = {f"{year}.º ano" for year in range(1, 13)}
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

    guardian_name = str(data.get("guardian_name") or "").strip()
    guardian_email = str(data.get("guardian_email") or "").strip().lower()
    parental_consent = data.get("parental_consent") is True

    if is_minor:
        if not guardian_name or len(guardian_name) > 255:
            return jsonify({"error": "Indique o nome do encarregado de educação."}), 400
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", guardian_email):
            return jsonify({"error": "Indique um email válido para o encarregado de educação."}), 400
        if len(guardian_email) > 255:
            return jsonify({"error": "O email do encarregado de educação é demasiado longo."}), 400
        if not parental_consent:
            return jsonify({"error": "É necessária autorização do encarregado de educação."}), 400
    else:
        guardian_name = None
        guardian_email = None
        parental_consent = False

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

    try:
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
            password=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.flush()
        db.session.add(RoleUser(user_id=user.id, role_id=user_role.id))
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Este email já está registado."}), 409
    except Exception:
        db.session.rollback()
        app.logger.exception("Erro ao criar a conta de utilizador.")
        return jsonify({"error": "Não foi possível concluir o registo. Tente novamente."}), 500

    message = (
        "Pedido de registo recebido. A conta ficará pendente de validação do consentimento parental."
        if is_minor
        else "Registo concluído com sucesso."
    )
    return jsonify({"message": message}), 201


if __name__ == "__main__":
    with app.app_context():
        upgrade(directory=os.path.join(os.path.dirname(__file__), "migrations"))
    app.run(debug=True, port=5000)
