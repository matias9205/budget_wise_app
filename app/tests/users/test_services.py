import pytest
from app.config.db import db
from app.tests.conftest import test_client
from app.users.models import User
from app.users.schemas import NewUserSchema, UpdateUser
from app.users.services import UserService

@pytest.fixture(scope="function")
def user_service(db_session):
    return UserService(db_session)

class TestUserService:
    def test_create_new_user(self, user_service):
        payload = NewUserSchema(
            name="Matias Mazparrote",
            age=33,
            email="matumazparrote@gmail.com",
            password="Paris-9205",
            country="Argentina",
            balance=3120000,
            role="User"
        )
        new_user = user_service.create_new_user(payload)
        assert new_user.email == payload.email

    def test_update_user(self, user_service):
        user_to_update = user_service.get_user(1)
        original_user_balance = user_to_update.balance
        payload = UpdateUser(
            age=45,
            balance=4545435555
        )
        updated_user = user_service.update_user(1, payload)
        assert updated_user.balance != original_user_balance
        assert updated_user.email == "usergeneric@gmail.com"
        assert isinstance(updated_user, User)

    def test_delete_user(self, user_service):
        user_to_delete = user_service.get_user(1)
        user_to_delete_email = user_to_delete.email
        user_to_delete_id = user_to_delete.id
        user_service.delete_user(1)
        assert user_to_delete.email == "usergeneric@gmail.com"
        assert isinstance(user_to_delete, User)
        deleted_user = user_service.get_user(user_to_delete_id)
        assert deleted_user is None