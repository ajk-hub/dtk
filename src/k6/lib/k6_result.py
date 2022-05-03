import json


class K6Config:
    req_per_second: float = 15
    req_success_percentage: float = 95
    req_duration_per_millisecond: float = 500

    header_title: str = "| TEST SCRIPT                                                  | Max Users | Total Req " \
                        "| Succeeded Req | Failed Req | RPS        | Succeeded Req (>=95%) | Req Duration (<=500ms) " \
                        "| PASS/FAIL |"
    header_filler: str = "|--------------------------------------------------------------|-----------|-----------" \
                         "|---------------|------------|------------|-----------------------|------------------------" \
                         "|-----------|"


class K6Result:

    def __init__(self, input_file_name: str, config: K6Config) -> None:
        metrics = self.get_metrics(input_file_name).get('metrics')

        self.test_name = self.get_test_name(input_file_name)

        self.vus = self.vus_max_value(metrics)

        self.reqs_count = self.http_reqs_count(metrics)
        self.reqs_per_second = self.http_reqs_rate(metrics)

        self.checks_success_count = self.checks_passes(metrics)
        self.checks_failed_count = self.checks_fails(metrics)
        self.checks_success_percentage = self.checks_value(metrics)

        self.req_duration_per_millisecond = self.http_req_duration_avg(metrics)
        self.status = self.get_status(config)

    @staticmethod
    def get_metrics(input_file_name) -> {}:
        with open(input_file_name, "r") as read_file:
            data = json.load(read_file)
        return data

    @staticmethod
    def vus_max_value(metrics) -> float:
        vus_max = metrics.get('vus_max')

        if vus_max:
            return vus_max.get('value', 0)
        else:
            return 0

    @staticmethod
    def http_reqs_count(metrics) -> float:
        http_reqs = metrics.get('http_reqs')

        if http_reqs:
            return http_reqs.get('count', 0)
        else:
            return 0

    @staticmethod
    def http_reqs_rate(metrics) -> float:
        http_reqs = metrics.get('http_reqs')

        if http_reqs:
            return round(http_reqs.get('rate', 0), 2)
        else:
            return 0

    @staticmethod
    def checks_passes(metrics) -> float:
        checks = metrics.get('checks')

        if checks:
            return checks.get('passes', 0)
        else:
            return 0

    @staticmethod
    def checks_fails(metrics) -> float:
        checks = metrics.get('checks')

        if checks:
            return checks.get('fails', 0)
        else:
            return 0

    @staticmethod
    def checks_value(metrics) -> float:
        checks = metrics.get('checks')

        if checks:
            return round(checks.get('value', 0) * 100, 2)
        else:
            return 0

    @staticmethod
    def http_req_duration_avg(metrics) -> float:
        http_req_duration = metrics.get('http_req_duration')

        if http_req_duration:
            return round(http_req_duration.get('avg', 0), 2)
        else:
            return 0

    def get_status(self, config: K6Config) -> bool:
        if (self.is_req_success_percentage_above_limit(config)
                or self.is_req_duration_above_limit(config)):
            return False
        else:
            return True

    @staticmethod
    def get_test_name(input_file_name: str) -> str:
        basename = input_file_name.split("/")[-1]
        return basename.split(".")[0]

    def is_req_success_percentage_above_limit(self, config: K6Config) -> bool:
        return self.checks_success_percentage < config.req_success_percentage

    def is_req_duration_above_limit(self, config: K6Config) -> bool:
        return self.req_duration_per_millisecond > config.req_duration_per_millisecond


class MDResult:

    def __init__(self, result: K6Result, config: K6Config):

        self.test_name = result.test_name
        self.vus = result.vus
        self.reqs_count = result.reqs_count
        self.checks_success_count = result.checks_success_count
        self.checks_failed_count = result.checks_failed_count

        self.reqs_per_second = self.format_md(result.reqs_per_second, '/s', False)

        self.reqs_success_percentage = self.format_md(
            result.checks_success_percentage, '%',
            result.is_req_success_percentage_above_limit(config)
        )

        self.reqs_duration_per_millisecond = self.format_md(
            result.req_duration_per_millisecond, 'ms',
            result.is_req_duration_above_limit(config)
        )

        self.status = self.get_status(result)

    @staticmethod
    def get_status(result: K6Result) -> str:
        if result.status:
            return "PASS"
        else:
            return "**FAIL**"

    @staticmethod
    def format_md(original: float, units: str, failed: bool):
        md_string = f'{original}{units}'

        if failed:
            return f'**{md_string}**'
        else:
            return f'{md_string}'
