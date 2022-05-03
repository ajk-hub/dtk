from src.k6.lib.k6_result import K6Config, K6Result, MDResult
from src.k6.lib.k6_result_writer import K6Writer


def write(result_dir: str, input_file_name: str, output_file_name: str):
    print(f'Writing k6 output in ........... {result_dir}/')
    print('Printing Results :')
    input_file_name = f'{result_dir}/{input_file_name}'
    output_file_name = f'{result_dir}/{output_file_name}'

    config = K6Config()
    result = K6Result(input_file_name, config)
    md_result = MDResult(result, config)

    K6Writer.write_results_in_md(output_file_name, config, md_result)
    K6Writer.write_results_to_json(output_file_name, result)
