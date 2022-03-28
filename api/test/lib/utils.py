from typing import List, Dict, Any
from sqlalchemy.orm import sessionmaker
from functools import lru_cache

from fastapi.testclient import TestClient
from ...api.schemas.user import UserCreateSchema
from ...api.schemas.role import RoleCreateSchema
from ...api.cruds import (
    user as crud_user,
    role as crud_role,
)


@lru_cache()
def get_token(
    client: TestClient,
    username: str = "admin",
    password: str = "admin1234"
):
    response = client.post(
        "/api/v1/token",
        {"username": username, "password": password}
    )
    if response.status_code != 200:
        raise Exception(f"{response.status_code}: {response.content}")
    return response.json()["access_token"]

def create_user(
    session_factory,
    username: str = "admin",
    password: str = "admin1234",
    roles: List[str] = ["ItemAdminRole"],
    is_superuser: bool = False,
):
    with session_factory() as session:
        user = crud_user.create_user_if_not_exists(
            session,
            UserCreateSchema(username=username, password=password),
        )
        for role in roles:
            role = crud_role.create_role(
                session,
                RoleCreateSchema(name=role)
            )
            user.roles.append(role)
        user.is_superuser = is_superuser
        session.add(user)
        session.commit()

def http_get(client, url: str) -> List[Dict[str, Any]]:
    token = get_token(client)
    response = client.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code != 200:
        raise Exception(f"{response.status_code}: {response.content}")
    return response.json()

def create_role(client, name: str, desc: str = "") -> Dict[str, Any]:
    token = get_token(client)
    response = client.post(
        f"/api/v1/roles/",
        json={
            "name": name,
            "description": desc
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code != 200:
        raise Exception(f"{response.status_code}: {response.content}")
    return response.json()
    