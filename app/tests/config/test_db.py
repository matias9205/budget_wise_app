from sqlalchemy import inspect

from app.config.db import db
from app.users.models import User

class TestDB:
    def test_tables_created(test_client):
        engine = db.create_db_connection()
        inspector = inspect(engine)
        expected_tables = [
            "users", "roles", "transactions", "categories", 
            "audit_logs"
        ]
        for table in expected_tables:
            print(f"TABLE {table} WAS CREATED")
            assert table in inspector.get_table_names()
