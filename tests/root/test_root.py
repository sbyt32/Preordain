from fastapi.testclient import TestClient
def test_root(client: TestClient):
    from preordain.exceptions import RootException
    import pytest

    response = client.get('/')
    assert response.status_code == 400
    response = response.json()
    assert response['resp'] == RootException.resp

# def test_base_model():
#     from preordain.models import BaseResponse
#     import pytest

#     with pytest.raises(ValueError):
#         BaseResponse()