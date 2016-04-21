import os
import pytest
import shutil
import subprocess

from codeclimate_test_reporter.components.reporter import Reporter
from codeclimate_test_reporter.components.argument_parser import ArgumentParser
from .utils import ApiMock


def test_run():
    os.environ["CODECLIMATE_API_HOST"] = "http://example.com"

    api_mock = ApiMock()
    api_mock.setup(200)

    parsed_args = ArgumentParser().parse_args(["--file", "./coverage.txt", "--token", "token"])
    reporter = Reporter(parsed_args)

    orig_dir = os.getcwd()
    os.chdir("./tests/fixtures")

    subprocess.call(["git", "init"])
    subprocess.call(["git", "config", "user.name", "Test User"])
    subprocess.call(["git", "config", "user.email", "test@example.com"])
    subprocess.call(["git", "commit", "--allow-empty", "--message", "init"])

    try:
        return_code = reporter.run()

        assert(return_code == 0)
    finally:
        del os.environ["CODECLIMATE_API_HOST"]
        os.chdir(orig_dir)
        shutil.rmtree("./tests/fixtures/.git")
