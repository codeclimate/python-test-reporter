import pytest

from ..components.ci import CI


def test_travis_data():
    env = {
        "TRAVIS": True,
        "TRAVIS_BRANCH": "master",
        "TRAVIS_JOB_ID": "4.1",
        "TRAVIS_PULL_REQUEST": "false"
    }

    expected_data = {
        "name": "travis-ci",
        "branch": env["TRAVIS_BRANCH"],
        "build_identifier": env["TRAVIS_JOB_ID"],
        "pull_request": env["TRAVIS_PULL_REQUEST"]
    }

    data = CI(env).data()

    assert data == expected_data

def test_circle_data():
    env = {
        "CIRCLECI": True,
        "CIRCLE_BRANCH": "master",
        "CIRCLE_BUILD_NUM": "123",
        "CIRCLE_SHA1": "7638417db6d59f3c431d3e1f261cc637155684cd"
    }

    expected_data = {
        "name": "circleci",
        "branch": env["CIRCLE_BRANCH"],
        "build_identifier": env["CIRCLE_BUILD_NUM"],
        "commit_sha": env["CIRCLE_SHA1"]
    }

    data = CI(env).data()

    assert data == expected_data

def test_ci_pick():
    assert CI({ "TRAVIS": True }).data()["name"] == "travis-ci"
    assert CI({ "CIRCLECI": True }).data()["name"] == "circleci"
    assert CI({ "SEMAPHORE": True }).data()["name"] == "semaphore"
    assert CI({ "JENKINS_URL": True }).data()["name"] == "jenkins"
    assert CI({ "TDDIUM": True }).data()["name"] == "tddium"
    assert CI({ "WERCKER": True }).data()["name"] == "wercker"
    assert CI({ "APPVEYOR": True }).data()["name"] == "appveyor"
    assert CI({ "CI_NAME": "DRONE" }).data()["name"] == "drone"
    assert CI({ "CI_NAME": "CODESHIP" }).data()["name"] == "codeship"
    assert CI({ "CI_NAME": "VEXOR" }).data()["name"] == "vexor"
    assert CI({ "BUILDKITE": True }).data()["name"] == "buildkite"
    assert CI({ "GITLAB_CI": True }).data()["name"] == "gitlab-ci"
