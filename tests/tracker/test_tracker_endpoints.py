# from fastapi.testclient import TestClient


# def test_add_to_track(client: TestClient):
#     from starlette.config import environ

#     # This actually corresponds to a real card
#     sample_uri = "b2b91418-5cbd-443d-9963-7e590dd0b6fc"
#     json_body = {"uri": sample_uri}
#     header = {"write": str(environ["WRITE_TOKEN"])}
#     response = client.post("/api/tracker/add", json=json_body, headers=header)
#     response
