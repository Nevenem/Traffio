import os
import tempfile

import pytest

from traffio import create_app
from traffio.db import init_db


@pytest.fixture
def client():
    """
    Makes a test client using Flask's libraries
    """
    app = create_app({"TESTING": True})

    with app.test_client() as client:
        yield client


def test_root(client):
    """
    Tests if the index page contains the welcome text
    """
    response = client.get("/")
    assert b"Welcome to Traffio" in response.data


def test_flashcard(client):
    """
    Tests if images are present in flashcard pages
    """
    response = client.get("/flashcard")
    assert b"<img" in response.data


def test_cookie_presence(client):
    """
    Tests if the test id cookie gets set
    """
    response = client.get("/test")
    cookies = response.headers.getlist("Set-Cookie")
    assert any(["TestId" in cookie for cookie in cookies])


def test_cookie_change(client):
    """
    Tests if the test id changes when user ends the test
    """
    response = client.get("/test")
    first_cookies = response.headers.getlist("Set-Cookie")
    response = client.get("/test/end")
    response = client.get("/test")
    second_cookies = response.headers.getlist("Set-Cookie")
    assert first_cookies[0] != second_cookies[0]
