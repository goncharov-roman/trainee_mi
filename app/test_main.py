import time

from fastapi.testclient import TestClient

from .main import app


client = TestClient(app)

phrase = "My_secret_phrase"
secret = "My_secret"
ttl = 5

def test_without_ttl_nowait():
    response = client.get(f"/generate?phrase={phrase}&secret={secret}")
    secret_key = response.json()["secret_key"]
    response = client.get(f"/secrets/{secret_key}?phrase={phrase}")
    secret_ = response.json()["secret"]
    assert secret_ == secret

    response = client.get(f"/secrets/{secret_key}?phrase={phrase}")
    assert response.json()["secret"] == None


def test_without_ttl_wait():
    response = client.get(f"/generate?phrase={phrase}&secret={secret}")
    secret_key = response.json()["secret_key"]
    time.sleep(70)
    response = client.get(f"/secrets/{secret_key}?phrase={phrase}")
    secret_ = response.json()["secret"]
    assert secret_ == secret

    response = client.get(f"/secrets/{secret_key}?phrase={phrase}")
    assert response.json()["secret"] == None


def test_with_ttl_nowait():
    response = client.get(f"/generate?phrase={phrase}&secret={secret}&ttl={ttl}")
    secret_key = response.json()["secret_key"]
    response = client.get(f"/secrets/{secret_key}?phrase={phrase}")
    secret_ = response.json()["secret"]
    assert secret_ == secret

    response = client.get(f"/secrets/{secret_key}?phrase={phrase}")
    assert response.json()["secret"] == None


def test_with_ttl_wait():
    response = client.get(f"/generate?phrase={phrase}&secret={secret}&ttl={ttl}")
    secret_key = response.json()["secret_key"]
    time.sleep(70)
    response = client.get(f"/secrets/{secret_key}?phrase={phrase}")
    secret_ = response.json()["secret"]

    assert secret_ == None