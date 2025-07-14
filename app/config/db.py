import time
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlmodel import SQLModel

from .config import settings

class Db:
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = None
        self.SessionLocal = None
        self.Base = SQLModel
        self.attemp = 0

    def create_db_connection(self, max_attempts: int = 10, delay: int = 10):
        while self.attemp < max_attempts:
            try:
                print(f"----------------DB URL: {self.db_url}------------------------")
                self.engine = create_engine(self.db_url, echo=True, pool_pre_ping=True)
                with self.engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
                print("✅ Conexión establecida con la base de datos.")
                return self.engine
            except OperationalError as e:
                self.attemp += 1
                print(f"⚠️ Error de conexión (intento {self.attemp}/{max_attempts}): {e}")
                time.sleep(delay)
    
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

db = Db(settings.DATABASE_URL)