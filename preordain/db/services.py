from sqlalchemy.engine.base import Engine
from preordain.database import database_engine_v2
from preordain.schema import PreordainBase


def create_tables(engine: Engine):
    PreordainBase.metadata.create_all(engine)
