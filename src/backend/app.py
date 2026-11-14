import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from db import db

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

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
)

db.init_app(app)


@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello World!"})


if __name__ == "__main__":
    try:
        with app.app_context():
            import models.user
            db.create_all()
    except Exception as e:
        print(f"Aviso ao inicializar base de dados: {e}")

    app.run(debug=True, port=5000)
