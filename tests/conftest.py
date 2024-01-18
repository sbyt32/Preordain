import pytest
from fastapi.testclient import TestClient
from starlette.config import environ
from sqlalchemy_utils import database_exists, drop_database, create_database

# Declaring this here means they won't be defined in the next line.
environ["DB_NAME"] = "price_tracker_v2_test"
environ["SEC_TOKEN"] = "testing"
environ["WRITE_TOKEN"] = "testing"
environ["PRICE_TOKEN"] = "testing"
environ["DASHBOARD"] = "False"

# Getting rest of environment variables.
from preordain import config
from preordain.v2.database import database_engine_v2
from preordain.v2.db.services import create_tables
from preordain.main import app
from .database import Session


# print(database_engine_v2.url)
@pytest.fixture(scope="module")
def setup_db():
    if database_exists(database_engine_v2.url):
        drop_database(database_engine_v2.url)

    create_tables(database_engine_v2)

    yield
    drop_database(database_engine_v2.url)


# This is for
@pytest.fixture(scope="function", autouse=True)
def session(setup_db):
    session = Session()
    session.begin_nested()
    yield session
    session.rollback()


@pytest.fixture(scope="function")
def client(session):
    yield TestClient(app)
