import os
import pytest
import shutil
import subprocess
import sys

if sys.version_info >= (3, 0):
    from io import StringIO
else:
    from StringIO import StringIO

from codeclimate_test_reporter.components.runner import Runner
from codeclimate_test_reporter.__init__ import __version__ as reporter_version
from .utils import ApiMock


def test_version():
    out = StringIO()
    runner = Runner(["--version"], out=out)

    return_code = runner.run()

    assert(return_code == 0)
    assert(out.getvalue().strip() == reporter_version)

def test_run():
    os.environ["CODECLIMATE_API_HOST"] = "http://example.com"

    api_mock = ApiMock()
    api_mock.setup(200)

    runner = Runner(["--file", "./coverage.txt", "--token", "token"])

    orig_dir = os.getcwd()
    os.chdir("./tests/fixtures")

    subprocess.call(["git", "init"])
    subprocess.call(["git", "config", "user.name", "Test User"])
    subprocess.call(["git", "config", "user.email", "test@example.com"])
    subprocess.call(["git", "commit", "--allow-empty", "--message", "init"])

    try:
        return_code = runner.run()

        assert(return_code == 0)
    finally:
        del os.environ["CODECLIMATE_API_HOST"]
        os.chdir(orig_dir)
        shutil.rmtree("./tests/fixtures/.git")
        api_mock.cleanup()

def test_run_api_500_error():
    os.environ["CODECLIMATE_API_HOST"] = "http://example.com"

    api_mock = ApiMock()
    api_mock.setup(500)

    err = StringIO()
    runner = Runner(["--file", "./coverage.txt", "--token", "token"], err=err)

    orig_dir = os.getcwd()
    os.chdir("./tests/fixtures")

    subprocess.call(["git", "init"])
    subprocess.call(["git", "config", "user.name", "Test User"])
    subprocess.call(["git", "config", "user.email", "test@example.com"])
    subprocess.call(["git", "commit", "--allow-empty", "--message", "init"])

    try:
        return_code = runner.run()

        assert(return_code == 1)
        assert("500 Server Error" in err.getvalue().strip())
    finally:
        del os.environ["CODECLIMATE_API_HOST"]
        os.chdir(orig_dir)
        shutil.rmtree("./tests/fixtures/.git")
        api_mock.cleanup()
