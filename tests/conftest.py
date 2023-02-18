import pytest
from fastapi.testclient import TestClient
from starlette.config import environ

environ["SEC_TOKEN"] = "testing"
environ["WRITE_TOKEN"] = "testing"
environ["PRICE_TOKEN"] = "testing"

from preordain import config


@pytest.fixture
def client():
    from preordain.main import app

    with TestClient(app) as test_client:
        yield test_client


# TODO: Pass this as a pytest fixture?
# from preordain.models import RespStrings