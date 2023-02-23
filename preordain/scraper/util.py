import re
import datetime
import time
from dateutil.parser import isoparse
from typing import Optional, Union
from dotenv import dotenv_values
import logging

log = logging.getLogger()


class EnvVars:
    def __init__(self) -> None:
        self.env_data = dotenv_values(".env")

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

    def get_env(self) -> None:
        return self.env_data


def _regex_check(date: str):
    "Check if both dates match the correct format. Raise an exception if not."
    pattern = (
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}.*[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{1,6}?\+[\d:]{5}"
    )
    format_check = re.search(pattern, date)

    if format_check:
        return date
    raise Exception(
        f"{date} is not in proper format. Example: 2023-01-19 06:04:27.236195+00:00"
    )


def check_date_to_update(
    last_update: str,
    update_freq: datetime.timedelta,
    current_time: Optional[str] = None,
):
    """
    Checks to see if something needs to be updated. Used in conjunction with the config files.

    Expected Format: `2023-01-19 06:04:27.236195+00:00`

    `current_time` is optional, it uses the time right now if left unused.
    """
    # First, check if Bool. If None, return True to force the update (it would fail otherwise).
    if last_update == "None":
        return True

    # Next, check if passed the optional variable current_time. This is mostly for testing, :P
    if not current_time:
        current_time = datetime.datetime.now(datetime.timezone.utc)
        _regex_check(last_update)
    else:
        for date in [last_update, current_time]:
            _regex_check(date)

        current_time = isoparse(current_time)

    if abs(isoparse(last_update) - current_time) >= update_freq:
        return True
    return False
    # * If all else fails, I want it return an error, but still have it continue


def timer(func):
    def inner(*args, **kwargs):
        start = time.perf_counter()  # ? Used for timing the length to parse everything

        func(*args, **kwargs)
        log.debug(
            f"Elapsed time: {time.perf_counter() - start}"
        )  # ? Sends length to parse to debug

    return inner
