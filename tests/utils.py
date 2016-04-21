import subprocess
import httpretty


class ApiMock:
    def setup(self, status_code):
        httpretty.enable()
        httpretty.register_uri(
            httpretty.POST,
            "http://example.com/test_reports",
            status=status_code,
            content_type="application/plain"
        )

    def cleanup(self):
        httpretty.disable()
        httpretty.reset()
