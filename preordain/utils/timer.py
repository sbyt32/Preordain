import time
import logging


def timer(func):
    def inner(*args, **kwargs):
        start = time.perf_counter()  # ? Used for timing the length to parse everything
        func(*args, **kwargs)
        log = logging.getLogger()
        log.debug(
            f"Elapsed time: {time.perf_counter() - start}"
        )  # ? Sends length to parse to debug

    return inner
