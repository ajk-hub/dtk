import json


class K6Config:
    req_per_second: float = 15
    req_status_count: float = 95
    req_duration: float = 500

    header_title: str = " | TEST SCRIPT                                                  |" \
                        "   RPS (>=15/s)   | 200 (>=95%) |  TIME (<=500ms)  |  PASS/FAIL |"
    header_filler: str = " | ------------------------------------------------------------ |" \
                         " ---------------- | ----------- | ---------------- | ---------- |"


class K6Result:

    def __init__(self, input_file_name: str, config: K6Config) -> None:
        metrics = self.get_metrics(input_file_name).get('metrics')

        self.test_name = self.get_test_name(input_file_name)
        self.req_per_second = self.http_reqs(metrics)
        self.req_status_count = self.checks(metrics)
        self.req_duration = self.http_req_duration(metrics)
        self.status = self.get_status(config)

    @staticmethod
    def get_metrics(input_file_name) -> {}:
        with open(input_file_name, "r") as read_file:
            data = json.load(read_file)
        return data

    @staticmethod
    def http_reqs(metrics) -> float:
        http_reqs = metrics.get('http_reqs')

        if http_reqs:
            return round(http_reqs.get('rate', 0), 2)
        else:
            return 0

    @staticmethod
    def checks(metrics) -> float:
        checks = metrics.get('checks')

        if checks:
            suc_req_count = checks.get('passes', 0)
            fail_req_count = checks.get('fails', 0)
            return round((suc_req_count * 100) / (suc_req_count + fail_req_count), 2)
        else:
            return 0

    @staticmethod
    def http_req_duration(metrics) -> float:
        http_req_duration = metrics.get('http_req_duration')

        if http_req_duration:
            return round(http_req_duration.get('avg', 0), 2)
        else:
            return 0

    def get_status(self, config: K6Config) -> bool:
        if (self.req_per_second < config.req_per_second
                or self.req_status_count < config.req_status_count
                or self.req_duration > config.req_duration):

            return False
        else:
            return True

    @staticmethod
    def get_test_name(input_file_name: str) -> str:
        basename = input_file_name.split("/")[-1]
        return basename.split(".")[0]


class MDResult:

    def __init__(self, result: K6Result, config: K6Config):

        self.test_name = result.test_name

        self.md_req_per_second = self.format_md(result.req_per_second, '/s',
                                                result.req_per_second < config.req_per_second)

        self.md_req_status_count = self.format_md(result.req_status_count, '%',
                                                  result.req_status_count < config.req_status_count)

        self.md_req_duration = self.format_md(result.req_duration, 'ms',
                                              result.req_duration > config.req_duration)

        self.md_status = self.get_status(result)

    @staticmethod
    def get_status(result: K6Result) -> str:
        if result.status:
            return "  PASS  "
        else:
            return "**FAIL**"

    @staticmethod
    def format_md(original: float, units: str, failed: bool):
        md_string = f'{original}{units}'

        if failed:
            return f'**{md_string}**'
        else:
            return f'  {md_string}  '
