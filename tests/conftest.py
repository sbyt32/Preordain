import pytest
from fastapi.testclient import TestClient
from starlette.config import environ

# Declaring this here means they won't be defined later.
environ["SEC_TOKEN"] = "testing"
environ["WRITE_TOKEN"] = "testing"
environ["PRICE_TOKEN"] = "testing"
environ["TESTING"] = "True"
environ["DASHBOARD"] = "False"

# later
from preordain import config


# This is for
@pytest.fixture(scope="session")
def db():
    pass


# @pytest.fixture
# def client():
#     from preordain.main import app

#     with TestClient(app) as test_client:
#         yield test_client
