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
    test_utils.create_user(SessionLocal)
    yield
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_create_success_csvNotcommon():
    token = test_utils.get_token(client)
    response = client.post(
        "/api/v1/items/",
        data={
            "name": "test_1",
            "is_common": "false",
            "data_format": "CSV",
        },
        files={
            "file": ("test.csv", "en,ja\nkonbanha,こんばんは")
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    expected = {
        'id': body["id"],
        'name': 'test_1',
        'is_common': False,
        'data_format': 'CSV',
        'content': 'en,ja\nkonbanha,こんばんは',
        'owner': True
    }
    assert body == expected

def test_create_success_tsvCommon():
    token = test_utils.get_token(client)
    response = client.post(
        "/api/v1/items/",
        data={
            "name": "test_2",
            "is_common": "true",
            "data_format": "TSV",
        },
        files={
            "file": ("test.csv", "en\tja\nkonbanha\tこんばんは")
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    expected = {
        'id': body["id"],
        'name': 'test_2',
        'is_common': True,
        'data_format': 'TSV',
        'content': 'en\tja\nkonbanha\tこんばんは',
        'owner': True
    }
    assert body == expected


def test_read_success_getAll():
    token = test_utils.get_token(client)
    response = client.get(
        "/api/v1/items/",
        json={"skip": 0, "limit": 10},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "id" in body[0]
    assert "name" in body[0]
    assert "is_common" in body[0]
    assert "data_format" in body[0]
    assert "owner" in body[0]
    assert "content" not in body[0]

def test_read_success_getById():
    id = 1
    token = test_utils.get_token(client)
    response = client.get(
        f"/api/v1/items/{id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    expected ={
        'id': id,
        'name': 'test_1',
        'is_common': False,
        'data_format': 'CSV',
        'content': 'en,ja\nkonbanha,こんばんは',
        'owner': True
    }
    assert response.json() == expected

def test_read_success_download():
    id = 1
    token = test_utils.get_token(client)
    response = client.get(
        f"/api/v1/items/{id}/download",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

def test_update_success():
    id = 1
    token = test_utils.get_token(client)
    response = client.put(
        f"/api/v1/items/{id}",
        data={
            "name": "test",
            "is_common": "true",
            "data_format": "TSV",
        },
        files={
            "file": ("test.csv", "en\tja\nkonbanha\tこんばんは")
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    expected ={
        "id": id,
        "name": "test",
        "is_common": True,
        "data_format": "TSV",
        "content": 'en\tja\nkonbanha\tこんばんは',
        "owner": True
    }
    assert response.json() == expected
    actual = test_utils.http_get(client, f"/api/v1/items/{id}")
    assert actual == expected

def test_update_error_notFound():
    token = test_utils.get_token(client)
    response = client.put(
        f"/api/v1/items/10000",
        data={
            "name": "test",
            "is_common": "true",
            "data_format": "TSV",
        },
        files={
            "file": ("test.csv", "en,ja\nkonbanha,こんばんは")
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "item not found"}

def test_delete_success():
    id = 1
    token = test_utils.get_token(client)
    response = client.delete(
        f"/api/v1/items/{id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"item_id": 1}

def test_delete_error_notFound():
    token = test_utils.get_token(client)
    response = client.delete(
        f"/api/v1/items/10000",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "item not found"}