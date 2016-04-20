from setuptools import Command, find_packages, setup
from subprocess import call

from codeclimate_test_reporter.__init__ import __version__ as reporter_version


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(["py.test", "--cov=codeclimate_test_reporter", "tests/"])
        raise SystemExit(errno)


setup(
    name="codeclimate-test-reporter",
    version=reporter_version,
    description="Report test coverage to Code Climate",
    url="http://github.com/codeclimate/python-test-reporter",
    author="Code Climate",
    author_email="hello@codeclimate.com",
    maintainer="Code Climate",
    maintainer_email="hello@codeclimate.com",
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
    cmdclass={"test": RunTests},
    entry_points={
        "console_scripts": [
            "codeclimate-test-reporter=codeclimate_test_reporter.__main__:run",
        ],
    },
    package_data={"codeclimate_test_reporter": ["VERSION"]},
    install_requires=["coverage>=4.0", "requests"],
)
