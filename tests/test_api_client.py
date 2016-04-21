import httpretty
import os
import pytest

from codeclimate_test_reporter.components.api_client import ApiClient


def test_post():
    httpretty.enable()
    httpretty.register_uri(
        httpretty.POST,
        "http://example.com/test_reports",
        status=200,
        body="ok",
        content_type="application/plain"
    )

    client = ApiClient(host="http://example.com")
    response = client.post({})

    assert(response.status_code == 200)

    httpretty.disable()
    httpretty.reset()

def test_env_host():
    os.environ["CODECLIMATE_API_HOST"] = "http://example.com"

    client = ApiClient()

    assert(client.host == "http://example.com")

    del os.environ["CODECLIMATE_API_HOST"]

def test_default_host():
    client = ApiClient()

    assert(client.host == "https://codeclimate.com")
