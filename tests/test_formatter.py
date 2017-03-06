import os
import pytest
import shutil
import subprocess

from codeclimate_test_reporter.components.formatter import Formatter
from codeclimate_test_reporter.components.payload_validator import PayloadValidator


def test_formatter():
    orig_dir = os.getcwd()
    os.chdir("./tests/fixtures")

    subprocess.call(["git", "init"])
    subprocess.call(["git", "config", "user.name", "Test User"])
    subprocess.call(["git", "config", "user.email", "test@example.com"])
    subprocess.call(["git", "commit", "--allow-empty", "--message", "init"])

    try:
        formatter = Formatter("coverage.xml")
        payload = formatter.payload()
        formatter_latin_1 = Formatter("coverage_for_latin_1_source.xml")
        payload_latin_1 = formatter_latin_1.payload()
    finally:
        os.chdir(orig_dir)
        shutil.rmtree("./tests/fixtures/.git")

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

    # Assertions for the latin 1 file
    assert type(payload_latin_1) is dict
    assert len(payload_latin_1["source_files"]) == 1

    assert source_file["line_counts"] == expected_line_counts
    assert source_file["covered_percent"] == 0.9
    assert source_file["covered_strength"] == 1.0
    assert source_file["coverage"] == expected_coverage

    assert PayloadValidator(payload_latin_1).validate()
