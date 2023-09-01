from fastapi.routing import Mount
from fastapi.staticfiles import StaticFiles
from starlette.config import Config, environ
from starlette.datastructures import Secret
from dateutil.relativedelta import relativedelta
from .logging_details import log_setup
import logging, sys, os, subprocess

log_setup()
log = logging.getLogger("preordain")

"""
    A way to read the .env file
"""
try:
    config = Config(".env")
    PROJECT = config("PROJECT", cast=str, default="Preordain")
    DB_EXISTS = config("DB_EXISTS", cast=bool)
    DB_HOST = config("DB_HOST", cast=Secret)
    DB_USER = config("DB_USER", cast=Secret)
    DB_PASS = config("DB_PASS", cast=Secret)
    DB_NAME = config("DB_NAME", cast=Secret)

    TCG_SALES = config("TCG_SALES", cast=str)
    # ? So, it's first a string, then needs to be cast as a datetime

    SEC_TOKEN = config("SEC_TOKEN", cast=Secret)
    WRITE_TOKEN = config("WRITE_TOKEN", cast=Secret)
    PRICE_TOKEN = config("PRICE_TOKEN", cast=Secret)

    # * Keep the days the same, this is to make sure that the database has time to scrape the data.
    UPDATE_OFFSET = relativedelta(days=+1, hour=0, minute=10, second=0, microsecond=0)

    TESTING = config("TESTING", cast=bool)
    DASHBOARD = config("DASHBOARD", cast=bool, default=True)


except KeyError as e:
    if not environ.get("TESTING"):
        log.critical(e)
        sys.exit(1)


API_CONFIG: dict[list | str] = {
    "title": PROJECT,
    "description": "Production Build.",
    "routes": [],
}
# V1
V1_DASHBOARD = "preordain/v1/static/preordain/dist"
FOLDER_PATH = "./preordain/v1/images/{type}/{set}/"

# V2
IMG_FOLDER_PATH_V2 = "./preordain/v2/images/files/{scryfall_uri}"
V2_DASHBOARD = "preordain/v2/static/preordain/dist"

if TESTING:
    DB_NAME = Secret("test_" + str(DB_NAME))
    API_CONFIG[
        "description"
    ] = "Environment for testing. This should be enabled if you are running tests or are needing the testing database. "

if DASHBOARD:
    # if os.path.exists(V1_DASHBOARD):
    #     API_CONFIG[
    #         "description"
    #     ] += "Dashboard Enabled, the dashboard should be available on the /dash part."
    #     API_CONFIG["routes"].append(
    #         Mount(
    #             "/v1/dash",
    #             app=StaticFiles(directory="preordain/v1/static/preordain/dist", html=True),
    #             name="dashboard",
    #         )
    #     )
    # else:
    #     log.warning("Dashboard failed to load! It is not built, please run npm run dev")
    # API_CONFIG["description"] += "Dashboard Enabled but not build!"

    # TODO: This should build the static files, which will then serve right after.
    if not os.path.exists(V2_DASHBOARD):
        log.warning("Dashboard failed to load! Building right now...")
        subprocess.Popen(
            "npm run dev --prefix preordain/v2/static/preordain/", shell=True
        )

    # API_CONFIG[
    #     "description"
    # ] += "Dashboard Enabled, the dashboard should be available on the /dash part."
    # API_CONFIG["routes"].append(
    #     Mount(
    #         "/v2/dash",
    #         app=StaticFiles(directory="preordain/v2/static/preordain/dist/", html=True),
    #         name="dashboard",
    #     )
    # )
    # subprocess.Popen(["npm", "run", "dev", "--prefix", "preordain/v2/static/preordain/"], shell=True)
