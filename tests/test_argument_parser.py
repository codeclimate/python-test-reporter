import pytest

from codeclimate_test_reporter.components.argument_parser import ArgumentParser


def test_parse_args_default():
    parsed_args = ArgumentParser().parse_args([])

    assert(parsed_args.file == "./.coverage")
    assert(parsed_args.token is None)
    assert(parsed_args.stdout is False)
    assert(parsed_args.debug is False)
    assert(parsed_args.version is False)

def test_parse_args_with_options():
    args = ["--version", "--debug", "--stdout", "--file", "file", "--token", "token"]
    parsed_args = ArgumentParser().parse_args(args)

    assert(parsed_args.debug)
    assert(parsed_args.file == "file")
    assert(parsed_args.token == "token")
    assert(parsed_args.stdout)
    assert(parsed_args.version)
