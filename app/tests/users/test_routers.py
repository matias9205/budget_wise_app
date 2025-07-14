from fastapi import Body
from fastapi.testclient import TestClient
import pytest

@pytest.fixture
def new_user_payload():
    return {
        "name": "User Generic",
        "age": 40,
        "email": "usergeneric@gmail.com",
        "password": "Paris-9205",
        "country": "Argentina",
        "balance": 2145567,
        "role": "User"
    }

@pytest.fixture
def update_user_payload():
    return {
        "age": 33,
        "balance": 4545433
    }

class TestUserRouter:
    def test_register_new_user(self, test_client: TestClient, new_user_payload):
        response = test_client.post("/users/new", json=new_user_payload)
        print("RESPONSE STATUS:", response.status_code)
        print("RESPONSE BODY:", response.json())
        assert response.status_code == 200
        assert response.json()["email"] == new_user_payload["email"]
        assert "transactions" in response.json()
        assert isinstance(response.json()["transactions"], list)

    def test_update_user(self, test_client: TestClient, update_user_payload):
        response = test_client.patch("/users/update", json=update_user_payload)
        print("RESPONSE STATUS:", response.status_code)
        print("RESPONSE BODY:", response.json())
        assert response.status_code == 200