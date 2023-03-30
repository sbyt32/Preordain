from functools import wraps
import time
import logging


def timer(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start = time.perf_counter()  # ? Used for timing the length to parse everything
        function = func(*args, **kwargs)
        log = logging.getLogger(__name__)
        # log.warning(
        #     f"Elapsed time: {time.perf_counter() - start}"
        # )  # ? Sends length to parse to debug
        print(f"Elapsed time: {time.perf_counter() - start}")
        return function

    return inner
