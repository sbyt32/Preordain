import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from preordain.logging_details import log_setup
from preordain.config import API_CONFIG, mountDashboard

# from preordain.v1.api import api_router
from preordain.api import api_router_v2

# * Logging Information
log_setup()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


app = FastAPI(**API_CONFIG)
mountDashboard()
# app.include_router(api_router, prefix="/v1")
app.include_router(api_router_v2)

# ? I really don't like this out in the open, but I'm leaving it here for testing.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
