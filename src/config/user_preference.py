import json
import os
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from src.config import constants
from src.lib.common import log_error, user_home


@dataclass_json
@dataclass
class UserPreference:
    ci_config: str
    base_domain: str
    docker_user: str
    docker_pass: str
    internal_url: str
    internal_image_prefix: str
    internal_user: str
    internal_pass: str
    sonar_url: str
    sonar_user: str
    sonar_pass: str
    helm_default_namespace: str
    helm_default_chart_path: str
    k6_ramp_up_duration: str
    k6_ramp_max_duration: str
    k6_ramp_down_duration: str
    k6_max_users: str
    k6_result_dir: str
    k6_result_file: str
    k6_api_gateway_url: str
    k6_secure_url: str
    k6_secure_username: str
    k6_secure_password: str


def load_user_preference(file_path: str) -> UserPreference:
    if not os.path.exists(file_path):
        log_error(f"{file_path} not found, please provide one!")

    try:
        with open(file_path) as user_preference_file:
            default_dict = json.load(user_preference_file)
            user_preference: UserPreference = UserPreference.from_dict(default_dict)
            return user_preference

    except Exception as e:
        log_error(f"Please provide value for {str(e)} field in {file_path} file!")


def get_user_preference() -> UserPreference:
    return load_user_preference(user_home(constants.USER_PREFERENCE_FILE))


if __name__ == '__main__':
    samples_file_path = os.path.abspath(f"{os.curdir}/../../samples")
    _user_preference = load_user_preference(f"{samples_file_path}/{constants.USER_PREFERENCE_FILE}")
    print(_user_preference)
