from sqlalchemy.engine.base import Engine
from preordain.v2.schema import PreordainBase
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Connection, DDL, event, Table


def create_tables(engine: Engine):
    if not database_exists(engine.url):
        create_database(engine.url)

    PreordainBase.metadata.create_all(engine)


# * This listens for schemas and creates them!
# ? I'm not sure the best place to put these, though.
@event.listens_for(Table, "before_create")
def create_schema_if_not_exists(target: Table, connection: Connection, **_):
    connection.execute(
        DDL("CREATE SCHEMA IF NOT EXISTS %(schema)s", {"schema": target.schema})
    )
