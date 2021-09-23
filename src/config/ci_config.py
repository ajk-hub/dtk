import os
from dataclasses import dataclass

import yaml
from dataclasses_json import dataclass_json

from src.config import constants
from src.config.user_preference import get_user_preference
from src.lib.common import log_error, expand_path


@dataclass_json
@dataclass
class CIConfig:
    DIR_DOCKER: str
    DIR_CHART: str


def load_ci_config(file_path: str) -> CIConfig:
    if not os.path.exists(file_path):
        log_error(f"'{file_path}' file not found, please provide one!")

    try:
        with open(file_path) as file:
            data = yaml.safe_load(file)
            proj_dict = data[constants.CI_CONFIG_VARIABLES_SECTION]
            return CIConfig.from_dict(proj_dict)

    except Exception as e:
        log_error(f"Please provide value for {str(e)} field in {file_path} file!")


def get_ci_config() -> CIConfig:
    user_preference = get_user_preference()
    return load_ci_config(expand_path(user_preference.ci_config))


if __name__ == '__main__':
    samples_file_path = os.path.abspath(f"{os.curdir}/../../samples")
    _ci_config = load_ci_config(f"{samples_file_path}/{constants.CI_CONFIG_FILE}")
    print(_ci_config)
