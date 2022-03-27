from fastapi.testclient import TestClient
import pytest

from main import app
from api.db.base import Base
from api.db.db import engine

client = TestClient(app)

# Dependencies Override
# https://fastapi.tiangolo.com/advanced/testing-dependencies/#testing-dependencies-with-overrides

"""setup/teardownのサンプル

@pytest.fixture(scope="function", autouse=True)
def pre_function():
    scope = "Function"
    print(f"\n[{scope}]: SETUP")
    yield
    print(f"\n[{scope}]: TEARDOWN")


@pytest.fixture(scope="class", autouse=True)
def pre_class():
    scope = "Class"
    print(f"\n[{scope}]: SETUP")
    yield
    print(f"\n[{scope}]: TEARDOWN")


@pytest.fixture(scope="module", autouse=True)
def pre_module():
    scope = "Module"
    print(f"\n[{scope}]: SETUP")
    yield
    print(f"\n[{scope}]: TEARDOWN")


@pytest.fixture(scope="package", autouse=True)
def pre_package():
    scope = "Package"
    print(f"\n[{scope}]: SETUP")
    yield
    print(f"\n[{scope}]: TEARDOWN")


@pytest.fixture(scope="session", autouse=True)
def pre_session():
    scope = "Session"
    print(f"\n[{scope}]: SETUP")
    yield
    print(f"\n[{scope}]: TEARDOWN")
"""

@pytest.fixture(scope="module", autouse=True)
def pre_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_read_healthcheck():
    response = client.get("/api/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"message": "healthy"}