import configparser
import os
import logging
from preordain.logging_details import log_setup

# TODO: Place all the setup stuff in a class
class SetUp:
    def __init__(self) -> None:
        log_setup()
        self.log = logging.getLogger(__name__)
        