import os
import psycopg2
from contextlib import contextmanager
from sqlalchemy import create_engine


class DatabaseManager:
    def __init__(self):
        # Use env vars so the same code works in Dev and Docker
        self.user = os.getenv("DB_USER", "postgres")
        self.password = os.getenv("DB_PASSWORD", "PASSword8!")
        self.host = os.getenv(
            "DB_HOST", "localhost"
        )  # 'localhost' for host, 'db_service_name' for Docker
        self.port = os.getenv("DB_PORT", "5432")
        self.dbname = os.getenv("DB_NAME", "postgres")

    @property
    def connection_string(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"

    def get_engine(self):
        url = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        return create_engine(url)

    @contextmanager
    def get_connection(self):
        conn = psycopg2.connect(self.connection_string)
        try:
            yield conn
        finally:
            conn.close()
