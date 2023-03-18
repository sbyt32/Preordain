import logging
from fastapi import FastAPI
from fastapi.routing import Mount
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from preordain.exceptions import (
    InvalidToken,
    token_exception_handler,
    RootException,
    root_exception_handler,
    NotFound,
    not_found_exception_handler,
)
from preordain.search.exceptions import InvalidSearchQuery, invalid_search_handler
from preordain.logging_details import log_setup
from preordain.config import PROJECT, TESTING
from preordain.api import api_router

# * Logging Information
log_setup()

log = logging.getLogger(__name__)
routes = [
    Mount(
        "/dash",
        app=StaticFiles(directory="preordain/static/preordain/dist", html=True),
        name="dashboard",
    ),
]
if TESTING:
    desc = "TESTING"
else:
    desc = "PROD-ISH"

app = FastAPI(title=PROJECT, description=desc, routes=routes)
app.include_router(api_router, prefix="/api")

# ? I really don't like this out in the open, but I'm leaving it here for testing.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ? Can this be done more efficently?

app.add_exception_handler(InvalidToken, token_exception_handler)
app.add_exception_handler(RootException, root_exception_handler)
app.add_exception_handler(InvalidSearchQuery, invalid_search_handler)
app.add_exception_handler(NotFound, not_found_exception_handler)
