from sqlalchemy.engine.base import Engine
from preordain.v2.database import database_engine_v2
from preordain.v2.schema import PreordainBase


def create_tables(engine: Engine):
    PreordainBase.metadata.create_all(engine)
