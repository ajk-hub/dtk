import glob
import os

from src.config.user_preference import get_user_preference, UserPreference
from src.k6.lib import k6_output
from src.lib import process

K6_CMD_STACK = ['k6']


class K6CommandHelper:

    @staticmethod
    def run(args):
        if str(args.script_path).endswith(".js"):
            args.file = args.script_path
            K6CommandHelper.run_k6(args)
        else:
            files = glob.glob(args.script_path + "/*.js")

            for file in files:
                print(f'\nRunning ................... {file}')
                args.file = file
                K6CommandHelper.run_k6(args)

    @staticmethod
    def run_k6(args):
        user_preference: UserPreference = get_user_preference()
        k6_summary_file = K6CommandHelper._get_result_file(args.file)

        ramp_up_duration = K6CommandHelper.if_or_else(args.ramp_up_duration, user_preference.k6_ramp_up_duration)
        ramp_max_duration = K6CommandHelper.if_or_else(args.ramp_max_duration, user_preference.k6_ramp_max_duration)
        ramp_down_duration = K6CommandHelper.if_or_else(args.ramp_down_duration, user_preference.k6_ramp_down_duration)
        max_users = K6CommandHelper.if_or_else(args.max_users, user_preference.k6_max_users)
        result_dir = K6CommandHelper.if_or_else(args.result_dir, user_preference.k6_result_dir)
        secure_url = K6CommandHelper.if_or_else(args.secure_url, user_preference.k6_secure_url)
        api_gateway_url = K6CommandHelper.if_or_else(args.api_gateway_url, user_preference.k6_api_gateway_url)
        username = K6CommandHelper.if_or_else(args.username, user_preference.k6_secure_username)
        password = K6CommandHelper.if_or_else(args.password, user_preference.k6_secure_password)
        result_file = K6CommandHelper.if_or_else(args.result_file, user_preference.k6_result_file)

        os.makedirs(result_dir, exist_ok=True)

        CMD_STACK = list(K6_CMD_STACK)
        CMD_STACK.append('run')
        CMD_STACK.append(f'--vus {max_users}')
        CMD_STACK.append(f'--stage {ramp_up_duration}s:{max_users}')
        CMD_STACK.append(f'--stage {ramp_max_duration}s:{max_users}')
        CMD_STACK.append(f'--stage {ramp_down_duration}s:0')
        CMD_STACK.append(f'--summary-export={result_dir}/{k6_summary_file}')
        CMD_STACK.append(f'--env SECURE_URL={secure_url}')
        CMD_STACK.append(f'--env API_GATEWAY_URL={api_gateway_url}')
        CMD_STACK.append(f'--env USERNAME={username}')
        CMD_STACK.append(f'--env PASSWORD={password}')
        CMD_STACK.append(f'{args.file}')

        if not args.verbose:
            CMD_STACK.append('>/dev/null')

        if args.print:
            print("Shell Command")
            print("==================================================================================")
            print(*CMD_STACK, sep=' ')
            print("==================================================================================")

        process.command(CMD_STACK)
        k6_output.write(result_dir, k6_summary_file, result_file)

    @staticmethod
    def _get_result_file(file: str) -> str:
        basename = file.split("/")[-1]
        return basename.split(".")[0] + '.json'

    @staticmethod
    def if_or_else(value, default):
        return value if value else default
