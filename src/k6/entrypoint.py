import sys
from argparse import ArgumentParser

from src.k6.k6_cmd_helper import K6CommandHelper


def _k6_run(args):
    K6CommandHelper.run(args)


def _register_arg_options(parser: ArgumentParser):
    k6_parser = parser.add_subparsers()

    k6_run_parser = k6_parser.add_parser('run')
    k6_run_parser.add_argument('script_path', help="script path")
    k6_run_parser.add_argument('--ramp_up_duration', help='Ramp up duration', default='', )
    k6_run_parser.add_argument('--ramp_max_duration', help='Ramp maximum duration', default='')
    k6_run_parser.add_argument('--ramp_down_duration', help='Ramp down duration', default='')
    k6_run_parser.add_argument('--max_users', help='Maximum user', default='')
    k6_run_parser.add_argument('--result_dir', help='Result path', default='')
    k6_run_parser.add_argument('--result_file', help='Result file name', default='')
    k6_run_parser.add_argument('--secure_url', help='Secure URL', default='')
    k6_run_parser.add_argument('--api_gateway_url', help='API Gateway Url', default='')
    k6_run_parser.add_argument('--username', help='Username', default='')
    k6_run_parser.add_argument('--password', help='Password', default='')
    k6_run_parser.add_argument('-v', '--verbose', help="verbose", action='store_true')

    k6_run_parser.set_defaults(func=_k6_run)

    if len(sys.argv) == 2 and 'k6' == sys.argv[1]:
        parser.print_help()
        sys.exit()

    if len(sys.argv) == 3 and 'k6' == sys.argv[1] and 'run' == sys.argv[2]:
        k6_run_parser.print_help()
        sys.exit()


def register(parser):
    k6_parser = parser.add_parser('k6')
    _register_arg_options(k6_parser)
