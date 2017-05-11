import os
import pytest
import shutil
import subprocess
import unittest

from codeclimate_test_reporter.components.formatter import Formatter
from codeclimate_test_reporter.components.formatter import InvalidReportVersion
from codeclimate_test_reporter.components.payload_validator import PayloadValidator


class FormatterTest(unittest.TestCase):
    def test_payload_latin_1(self):
        orig_dir = os.getcwd()
        os.chdir("./tests/fixtures")

        self.__setup_git()

        try:
            formatter = Formatter("coverage_for_latin_1_source.xml")
            payload = formatter.payload()
        finally:
            os.chdir(orig_dir)
            shutil.rmtree("./tests/fixtures/.git")

        source_file = payload["source_files"][0]
        expected_line_counts = {"covered": 9, "missed": 1, "total": 10}
        expected_coverage = "[null, null, null, null, 1, 1, 1, 1, null, 1, 1, null, 1, 0, null, 1, 1]"

        assert type(payload) is dict
        assert len(payload["source_files"]) == 1

        assert source_file["line_counts"] == expected_line_counts
        assert source_file["covered_percent"] == 0.9
        assert source_file["covered_strength"] == 1.0
        assert source_file["coverage"] == expected_coverage

        assert PayloadValidator(payload).validate()

    def test_payload(self):
        orig_dir = os.getcwd()
        os.chdir("./tests/fixtures")

        self.__setup_git()

        try:
            formatter = Formatter("coverage.xml")
            payload = formatter.payload()
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

    def test_payload_incompatible_version(self):
        orig_dir = os.getcwd()
        os.chdir("./tests/fixtures")

        try:
            formatter = Formatter("coverage_invalid_version.xml")
            self.assertRaises(InvalidReportVersion, formatter.payload)
        finally:
            os.chdir(orig_dir)

    def __setup_git(self):
        subprocess.call(["git", "init"])
        subprocess.call(["git", "config", "user.name", "Test User"])
        subprocess.call(["git", "config", "user.email", "test@example.com"])
        subprocess.call(["git", "commit", "--allow-empty", "--message", "init"])
