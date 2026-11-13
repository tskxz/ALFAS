import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_db_connection(with_db=True):
    """
    Retorna uma nova conexão à base de dados MySQL.
    """
    user = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    host = os.environ.get("DB_HOST") or "127.0.0.1"
    port = int(os.environ.get("DB_PORT") or 3306)

    config = {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
    }

    if with_db:
        database = os.environ.get("DB_DATABASE")
        config["database"] = database

    return mysql.connector.connect(**config)


if __name__ == "__main__":
    try:
        cnx = get_db_connection(with_db=False)
        print("Ligação ao MySQL estabelecida com sucesso.")
        cnx.close()
    except Exception as e:
        print(f"Erro na ligação ao MySQL: {e}")
