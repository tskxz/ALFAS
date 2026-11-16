import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate, upgrade
from dotenv import load_dotenv
import mysql.connector
from db import db

# Load models so Flask-Migrate can discover their tables.
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

with app.app_context():
    db.create_all()

migrate = Migrate(app, db)


@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello World!"})


if __name__ == "__main__":
    with app.app_context():
        upgrade(directory=os.path.join(os.path.dirname(__file__), "migrations"))
    app.run(debug=True, port=5000)
