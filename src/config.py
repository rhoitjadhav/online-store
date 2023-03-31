import os

# Static Files
STATIC_FILES_PATH = "static"

# Postgresql
SQLALCHEMY_DATABASE_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL", "sqlite:///./store.db")
# "SQLALCHEMY_DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/store")
