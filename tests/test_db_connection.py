import psycopg
from preordain import config
# TODO: Eventually


db_info = dict(
        zip (   ('host','user', 'password', 'dbname'), 
                (str(config.DB_HOST), str(config.USER), str(config.PASSWORD), str(config.DB_NAME))
            ))
conn_info = psycopg.conninfo.make_conninfo(**db_info)
with psycopg.connect(conn_info) as conn:

    with conn.cursor() as cur:

        # Create a temporary table to test some stuff out.
        cur.execute("""
            CREATE TEMP TABLE pytest_sample (
                id serial PRIMARY KEY,
                num integer,
                data text)
            """)

        # Insert some data into the temporary table.
        cur.execute(
            "INSERT INTO pytest_sample (num, data) VALUES (%s, %s)",
            (100, "abc'def"))

        # Query the database and obtain data as Python objects.
        cur.execute("SELECT * FROM pytest_sample")
        # * This will return (1, 100, "abc'def")

        assert cur.fetchone() == (1, 100, "abc'def")
