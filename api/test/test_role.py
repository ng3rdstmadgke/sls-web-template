from fastapi.testclient import TestClient
import pytest

from ..main import app
from ..api.db.base import Base
from ..api.db.db import engine, SessionLocal
from .lib import utils as test_utils


client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def pre_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    test_utils.create_user(
        session_factory=SessionLocal,
        is_superuser=True,
    )
    yield
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_create_success():
    token = test_utils.get_token(client)
    response = client.post(
        "/api/v1/roles/",
        json={
            "name": "TestRole",
            "description": "test",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    expected = {
        'id': 2,
        'name': "TestRole",
        'description': "test",
    }
    assert response.json() == expected

def test_create_error_alreadyExists():
    token = test_utils.get_token(client)
    response = client.post(
        "/api/v1/roles/",
        json={
            "name": "TestRole",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Role already registerd"}


def test_read_success_getAll():
    token = test_utils.get_token(client)
    response = client.get(
        "/api/v1/roles/",
        json={"skip": 0, "limit": 10},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_read_success_getById():
    id = 2
    token = test_utils.get_token(client)
    response = client.get(
        f"/api/v1/roles/{id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    expected = {
        'id': id,
        'name': "TestRole",
        'description': "test",
    }
    assert response.json() == expected

def test_read_error_notFound():
    id = 10000
    token = test_utils.get_token(client)
    response = client.get(
        f"/api/v1/roles/{id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404

def test_update_success():
    id = 2
    token = test_utils.get_token(client)
    response = client.put(
        f"/api/v1/roles/{id}",
        json={
            "name": "TestUpdatedRole",
            "description": "test updated",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    expected ={
        "id": id,
        "name": "TestUpdatedRole",
        "description": "test updated",
    }
    assert response.json() == expected
    actual = test_utils.http_get(client, f"/api/v1/roles/{id}")
    assert actual == expected

def test_update_error_notFound():
    id = 10000
    token = test_utils.get_token(client)
    response = client.put(
        f"/api/v1/roles/{id}",
        json={
            "name": "TestUpdatedRole",
            "description": "test updated",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404

def test_delete_success():
    id = 2
    token = test_utils.get_token(client)
    response = client.delete(
        f"/api/v1/roles/{id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"role_id": id}

def test_delete_error_notFound():
    id = 10000
    token = test_utils.get_token(client)
    response = client.delete(
        f"/api/v1/roles/10000",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
