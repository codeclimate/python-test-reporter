import coverage as Coverage
import json
import os
import sys

from ..components.api_client import ApiClient
from ..components.formatter import Formatter
from ..components.payload_validator import PayloadValidator


class CoverageFileNotFound(Exception):
    pass


class Reporter:
    def __init__(self, args):
        self.args = args

    def run(self):
        """
        The main program without error handling

        :param args: parsed args (argparse.Namespace)
        :return: status code

        """

        if not os.path.isfile(self.args.file):
            message = "Coverage file `" + self.args.file + "` file not found. "
            raise CoverageFileNotFound(message)

        xml_filepath = self.__create_xml_report(self.args.file)
        formatter = Formatter(xml_filepath)
        payload = formatter.payload()

        PayloadValidator(payload).validate()

        if self.args.stdout:
            print(json.dumps(payload))

            return 0
        else:
            client = ApiClient()

            print("Submitting payload to %s" % client.host)

            response = self.__post_payload(client, payload)

            return response

    def __post_payload(self, client, payload):
        payload["repo_token"] = self.args.token or os.environ.get("CODECLIMATE_REPO_TOKEN")

        if payload["repo_token"]:
            response = client.post(payload)
            response.raise_for_status()

            return 0
        else:
            print("CODECLIMATE_REPO_TOKEN is required and not set")

            return 1

    def __create_xml_report(self, file):
        cov = Coverage.coverage(file)
        cov.load()
        data = cov.get_data()

        xml_filepath = "/tmp/coverage.xml"
        cov.xml_report(outfile=xml_filepath)

        return xml_filepath

    def __exit_code_for_status_code(self, status_code):
        if status_code == 200:
            return 0
        elif status_code == 500:
            return 1
