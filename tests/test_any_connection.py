# TODO: Figure out how to correctly write tests
from scripts.connect.to_requests_wrapper import send_response

result = send_response("GET", "https://httpbin.org/json")

assert bool(result)