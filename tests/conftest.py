import os

import pytest
# import requests
from fastapi.testclient import TestClient

# set ENV before create the app, to make sure we are creating a test db
os.environ["ENV"] = "TEST"
from main import app


@pytest.fixture(scope="session")
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="session", autouse=True)
def clear_db_teardown():
    # code before yield statement will excute before the first test
    yield None
    # code after yield statement will excute after the last test
    os.remove("fastapi_app_test.db")


# @pytest.fixture(scope="session")
# def superuser_access_token():
#     login_data = {"username": "super.user@example.com", "password": "passw0rd"}
#     response = requests.post("/auth/token", data=login_data)
#     yield response.json()["access_token"]
