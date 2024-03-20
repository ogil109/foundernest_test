import os


class Config:
    # Docker container config
    CONT_NAME = "postgres_container_oscar"
    IMAGE = "postgres:15"
    DB_USER = "user"
    DB_PASS = "pass"
    DB_NAME = "challenge"
    VOLUME_NAME = "challenge_data"

    # SQLAlchemy Postgres database config
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASS = os.environ.get("DB_PASS", "demo")
