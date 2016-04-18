import pytest
import subprocess

from ..components.formatter import Formatter
from ..components.payload_validator import PayloadValidator


def test_formatter():
    subprocess.call(["git", "config", "--global", "user.email", "you@example.com"])
    subprocess.call(["git", "config", "--global", "user.name", "Your Name"])
    subprocess.call(["git", "init"])
    subprocess.call(["git", "add", "."])
    subprocess.call(["git", "commit", "-m", "init"])

    formatter = Formatter("./reporter/tests/fixtures/coverage.xml")
    payload = formatter.payload()

    assert type(payload) is dict
    assert len(payload["source_files"]) == 1

    source_file = payload["source_files"][0]
    expected_line_counts = {"covered": 9, "missed": 1, "total": 10}
    expected_coverage = "[null, null, null, 1, 1, 1, 1, null, 1, 1, null, 1, 0, null, 1, 1]"

    assert source_file["line_counts"] == expected_line_counts
    assert source_file["covered_percent"] == 0.9
    assert source_file["covered_strength"] == 1.0
    assert source_file["coverage"] == expected_coverage

    assert PayloadValidator(payload).validate()
