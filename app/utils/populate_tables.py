from sqlalchemy import create_engine
from sqlmodel import Session

from app.categories.models import Category
from app.users.models import User
from app.transactions.models import Transaction
from app.roles.models import Role
from app.audit_logs.models import AuditLog

class PopulateTable:
    def __init__(self, engine: create_engine):
        self.engine = engine
        self.categories_list = ['Alquiler', 'Expensas', 'Facturas de servicios', 'Viajes', 'Compras', 'Sueldos']
        self.roles_list = ['Admin', 'User', 'Viewer', 'Service']

    def populate_categories(self):
        with Session(self.engine) as session:
            existing = session.query(Category).count()
            find_categories = [category.name for category in session.query(Category).filter(Category.name.in_(self.categories_list)).all()]
            print(f"CATEGORIES IN DB: {find_categories}")
            for cat in self.categories_list:
                if existing == 0 or cat not in find_categories:
                    session.add(Category(name=cat))
                    session.commit()

    def populate_roles(self):
        with Session(self.engine) as session:
            existing = session.query(Role).count()
            find_roles = [role.name for role in session.query(Role).filter(Role.name.in_(self.roles_list)).all()]
            print(f"ROLES IN DB: {find_roles}")
            for role in self.roles_list:
                if existing == 0 or role not in find_roles:
                    session.add(Role(name=role))
                    session.commit()
