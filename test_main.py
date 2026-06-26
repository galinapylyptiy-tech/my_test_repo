import copy

import pytest
from fastapi.testclient import TestClient

import main

client = TestClient(main.app)
initial_db = copy.deepcopy(main.db)


@pytest.fixture(autouse=True)
def reset_db():
    main.db = copy.deepcopy(initial_db)
    yield


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "Galina"}


def test_get_users():
    response = client.get("/api/v1/users")
    assert response.status_code == 200

    users = response.json()
    assert isinstance(users, list)
    assert len(users) == len(initial_db)
    assert users[0]["first_name"] == "John"
    assert users[0]["gender"] == "male"
    assert users[0]["roles"] == ["admin", "user"]


def test_create_user():
    user_payload = {
        "first_name": "Maria",
        "last_name": "Ivanova",
        "middle_name": "Petrovna",
        "gender": "female",
        "roles": ["user", "student"],
    }

    response = client.post("/api/v1/users", json=user_payload)
    assert response.status_code == 200
    assert "id" in response.json()

    users = client.get("/api/v1/users").json()
    assert len(users) == len(initial_db) + 1
    assert any(user["first_name"] == "Maria" for user in users)


def test_delete_user():
    user_id = str(main.db[0].id)

    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert f"User with ID {user_id} was deleted successfully" in response.json()["message"]

    users = client.get("/api/v1/users").json()
    assert len(users) == len(initial_db) - 1
    assert all(user["id"] != user_id for user in users)


def test_delete_user_not_found():
    response = client.delete("/api/v1/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json()["detail"] == "User with ID 00000000-0000-0000-0000-000000000000 is not found"


def test_update_user():
    user_id = str(main.db[1].id)
    updated_payload = {
        "id": user_id,
        "first_name": "Anna",
        "last_name": "Smith",
        "middle_name": "Maria",
        "gender": "female",
        "roles": ["admin"],
    }

    response = client.put(f"/api/v1/users/{user_id}", json=updated_payload)
    assert response.status_code == 200
    assert f"User with ID {user_id} was updated successfully" in response.json()["message"]

    users = client.get("/api/v1/users").json()
    assert any(user["id"] == user_id and user["roles"] == ["admin"] for user in users)
