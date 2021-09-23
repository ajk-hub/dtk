import json
import os

from src.k6.lib.k6_result import K6Config, K6Result, MDResult


class K6Writer:
    @staticmethod
    def write_results_in_md(output_file_name: str, config: K6Config, md_result: MDResult):
        K6Writer.write_header_in_md(output_file_name, config)
        K6Writer.write_k6_results_in_md(output_file_name, md_result)

    @staticmethod
    def write_header_in_md(output_file_name: str, config: K6Config):
        print(config.header_title)
        print(config.header_filler)

        if not os.path.exists(f"{output_file_name}.md"):
            with open(f"{output_file_name}.md", "w") as md_file:
                print(config.header_title, file=md_file)
                print(config.header_filler, file=md_file)

    @staticmethod
    def write_k6_results_in_md(output_file_name: str, md_result: MDResult):
        md_status = f" | {md_result.test_name:60} | {md_result.md_req_per_second:>16} " \
                    f"| {md_result.md_req_status_count:>11} | {md_result.md_req_duration:>16} " \
                    f"| {md_result.md_status:10} |"
        print(md_status)

        with open(f"{output_file_name}.md", "a") as md_file:
            print(md_status, file=md_file)

    @staticmethod
    def get_existing_json_results(output_file_name: str) -> []:
        all_results = []

        if os.path.exists(f"{output_file_name}.json"):
            with open(f"{output_file_name}.json", "r") as json_file:
                all_results = json.load(json_file)

        return all_results

    @staticmethod
    def write_results_to_json(output_file_name: str, result: K6Result):
        result = {
            "test_script": result.test_name,
            "request_per_second": f'{result.req_per_second}/s',
            "success_rate": f'{result.req_status_count}%',
            "request_duration": f'{result.req_duration}ms',
            "status": 'pass' if result.status else 'fail'
        }

        all_results = K6Writer.get_existing_json_results(output_file_name)
        all_results.append(result)

        with open(f"{output_file_name}.json", "w") as json_file:
            json.dump(all_results, json_file, indent=4)
