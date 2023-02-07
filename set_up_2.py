import configparser
import os
import logging
from preordain.logging_details import log_setup

class SetUp:
    def __init__(self) -> None:
        log_setup()
        self.log = logging.getLogger(__name__)
        