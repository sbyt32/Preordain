import getpass
import logging
import os
import psycopg
import requests
import secrets
from dotenv import dotenv_values
from psycopg import sql
from psycopg.rows import dict_row
from typing import Union

log = logging.getLogger(__name__)

class BaseSetup:
    def __init__(self, env_data: dict[str, Union[str, None]]) -> None:
        self.env_data = env_data

    def write_env(self):
        with open(".env", "w") as env_file:
            for k, v in self.env_data.items():
                print(f"{str(k)}={str(v)}\n")
                env_file.write(f"{str(k)}={str(v)}\n")
        env_file.close()

    def update_env(self, var: str, new_val: Union[str, bool]):
        """
        This one updates an existing variable, then calls the write_env to update.
        """
        self.env_data[var] = new_val
        self.write_env()

    def connect_to_db(self):
        db_info = dict(
            zip(
                ("host", "user", "password", "dbname"),
                (
                    str(self.env_data["DB_HOST"]),
                    str(self.env_data["DB_USER"]),
                    str(self.env_data["DB_PASS"]),
                    str(self.env_data["DB_NAME"]),
                ),
            )
        )
        log.debug(f"Connecting to database: {self.env_data['DB_NAME']}")
        conn_info = psycopg.conninfo.make_conninfo(**db_info)

        self.conn = psycopg.connect(conn_info, row_factory=dict_row)
        self.cur = self.conn.cursor()

        return self.conn, self.cur

    def close_db(self):
        log.debug(f"Comitting commands to Database {self.env_data['DB_NAME']}")
        self.conn.commit()
        log.debug(f"Closing connection to Database {self.env_data['DB_NAME']}")
        self.conn.close()

        self.update_env("DB_EXISTS", "true")

    def send_response(method: str, url: str, **kwargs):
        r = requests.request(method, url, **kwargs)
        log.debug(f"Sending a {method} to {url} with kwargs: {kwargs}")
        if not r.ok:
            log.error(f"Request failed! Status code:{r.status_code}")
        else:
            card_list = r.json()
            return card_list


class SetUp(BaseSetup):
    def __init__(self) -> None:
        self.env_data = {
            "PROJECT": "Preordain",
            "TCG_SALES": "None",
            "PRICE_FETCH": "None",
        }
        if os.path.exists(".env"):
            self.env_data = dotenv_values(".env")

    def check_path(self):
        env_reconfig = " "
        if os.path.exists(".env"):
            log.warning("User attempting to rewrite config.")
            env_reconfig = (
                input(
                    """.env already exists, replace?
            \nWarning! This overrides and replaces TCG_SALES and PRICE_FETCH! y/n """
                ).lower()
                or "n"
            )
        if not os.path.exists(".env") or env_reconfig[0].lower() == "y":
            cfg_log_msg = "creating .env"
            if env_reconfig[0].lower() == "y":
                cfg_log_msg = "Overwriting config.env"

            log.info(cfg_log_msg)
            return True
        return False

    def env_setup(self):
        self.env_data["DB_EXISTS"] = "false"
        if input("Create Database? y/n ")[0].lower() == "n":
            self.env_data["DB_EXISTS"] = "true"
        self.env_data["DB_HOST"] = (
            input("Host Address: (Default: localhost) ") or "localhost"
        )
        self.env_data["DB_USER"] = input("Username: ")
        self.env_data["DB_PASS"] = getpass.getpass(
            f"Password for {self.env_data['DB_USER']}: "
        )
        self.env_data["DB_NAME"] = (
            input("Database: (Default: price_tracker) ") or "price_tracker"
        )

        log.info("Generating some tokens...")
        self.env_data["SEC_TOKEN"] = secrets.token_urlsafe(16)
        self.env_data["WRITE_TOKEN"] = secrets.token_urlsafe(16)
        self.env_data["PRICE_TOKEN"] = secrets.token_urlsafe(16)

        BaseSetup.write_env(self)


class DatabaseSetup(BaseSetup):
    def __init__(self) -> None:
        if not os.path.exists(".env"):
            raise FileNotFoundError(".env file missing.")
        self.env_data = dotenv_values(".env")
        self.env_data["DB_HOST"] = os.environ.get("DB_HOST")

    def create_db_then_connect_db(self):
        if self.env_data["DB_EXISTS"] == "true":
            return
        conn = psycopg.connect(
            f"host={self.env_data['DB_HOST']} user={self.env_data['DB_USER']} password={self.env_data['DB_PASS']}"
        )
        cur = conn.cursor()

        conn.autocommit = True
        try:
            cur.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(self.env_data["DB_NAME"])
                )
            )
            db_create = f"Creating database: {self.env_data['DB_NAME']}"
        except psycopg.errors.DuplicateDatabase:
            db_create = f'Database "{self.env_data["DB_NAME"]}" already exists.'
        finally:
            log.debug(db_create)
        conn.close()

        self.conn, self.cur = BaseSetup.connect_to_db(self)

    def create_schema_card_info(self):
        self.cur.execute("CREATE SCHEMA IF NOT EXISTS card_info")
        log.debug('Creating schema "card_info" if it does not exist')

    def create_table_card_info_info(self):
        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS card_info.info
        (
            name            varchar(255),
            set             varchar(12),
            id              text,
            uri             text,
            tcg_id          text,
            tcg_id_etch     text,
            groups          text[],
            new_search      boolean
        )"""
        )
        log.debug('Creating table "card_info.info" if it does not exist')

    def create_table_public_card_data(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS card_data 
        (
            set         varchar(12) NOT NULL,
            id          text        NOT NULL,
            date        date        NOT NULL,
            usd         float(2),
            usd_foil    float(2),
            usd_etch    float(2),
            euro        float(2),
            euro_foil   float(2),
            tix         float(2)
        )"""
        )
        log.debug('Creating table "card_data" if it does not exist')

    def create_table_card_info_sets(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS card_info.sets
        (
            set             varchar(12) NOT NULL PRIMARY KEY,
            set_full        text        NOT NULL,
            release_date    date
        )"""
        )

        log.debug('Creating table "card_info.sets" if it does not exist')

        for sets in BaseSetup.send_response("GET", "https://api.scryfall.com/sets")[
            "data"
        ]:
            if not sets["digital"]:
                log.debug(f"Inserting {sets['name']} into card_info.sets")
                self.cur.execute(
                    """
                    INSERT INTO card_info.sets (set, set_full, release_date)

                    VALUES (%s, %s, %s)
                    
                    ON CONFLICT DO NOTHING
                    """,
                    (sets["code"], sets["name"], sets["released_at"]),
                )
                continue
            log.debug(f"Not inserting {sets['name']}: Set is digital-only.")

    def create_table_card_info_groups(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS card_info.groups
        (
            group_name  text    NOT NULL,        
            description text    NOT NULL,

            UNIQUE(group_name)
        )
        """
        )
        log.debug('Creating table "card_info.groups" if it does not exist')

    def create_table_public_card_data_tcg(self):
        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS card_data_tcg
        (
            order_id    varchar     NOT NULL,
            tcg_id      text        NOT NULL,
            order_date  timestamptz NOT NULL,
            condition   text        NOT NULL,
            variant     text        NOT NULL,
            qty         smallint    NOT NULL,
            buy_price   float(2)    NOT NULL,
            ship_price  float(2)    NOT NULL,
        
            UNIQUE(order_id)
        )
        """
        )
        log.debug('Creating table "card_data_tcg" if it does not exist')

    def create_field_types(self):
        field_types = [
            (
                """CREATE TYPE condition AS ENUM 
        (
            'NM','LP','MP','HP','DMG','SEAL'
        )
        """,
                "Condition",
            ),
            (
                """CREATE TYPE variant AS ENUM 
        (
            'Normal','Foil','Etched'
        )
        """,
                "Variant",
            ),
        ]
        log.debug("Creating types for condition and variants")

        with self.conn.transaction() as tx1:
            for operation in field_types:
                try:
                    with self.conn.transaction():
                        tx1.connection.execute(operation[0])
                except psycopg.errors.DuplicateObject:
                    log.debug(f"Type '{operation[1]}' already exists")
                else:
                    log.debug(f"Type '{operation[1]}' created")

    def create_table_public_inventory(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS inventory
            (
                add_date        date,
                tcg_id          text        NOT NULL,
                qty             int,
                buy_price       float(2),
                card_condition  condition,
                card_variant    variant
            )
            """
        )
        log.debug('Creating table "inventory" if it does not exist')


if __name__ == "__main__":
    set_up = SetUp()
    if set_up.check_path():
        set_up.env_setup()


    if set_up.env_data["DB_EXISTS"] == "false":
        db = DatabaseSetup()
        db.create_db_then_connect_db()
        db.create_schema_card_info()
        db.create_table_card_info_info()
        db.create_table_public_card_data()
        db.create_table_card_info_sets()
        db.create_table_public_card_data_tcg()
        db.create_field_types()
        db.create_table_public_inventory()
        db.close_db()
