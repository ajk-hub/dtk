import sys
from argparse import ArgumentParser

from src.helm.helm_cmd_helper import HELM_CMD_STACK
from src.helm.helm_cmd_helper import HelmCommandHelper as Helm
from src.lib import process


@Helm.list
def _helm_list(args):
    process.execute(HELM_CMD_STACK)


@Helm.status
def _helm_status(args):
    process.execute(HELM_CMD_STACK)


@Helm.deploy
def _helm_deploy(args):
    process.execute(HELM_CMD_STACK)


@Helm.delete
def _helm_delete(args):
    process.execute(HELM_CMD_STACK)


def _register_arg_options(parser: ArgumentParser):
    helm_parser = parser.add_subparsers()

    helm_list_parser = helm_parser.add_parser('list')
    helm_list_parser.set_defaults(func=_helm_list)

    helm_status_parser = helm_parser.add_parser('status')
    helm_status_parser.add_argument('-d', '--debug', help="debug", action='store_true')
    helm_status_parser.add_argument('-s', '--desc', help="show desc", action='store_true')
    helm_status_parser.add_argument('release_name', help="release name")
    helm_status_parser.set_defaults(func=_helm_status)

    helm_deploy_parser = helm_parser.add_parser('deploy')
    helm_deploy_parser.add_argument('release_name', help="release name")
    helm_deploy_parser.add_argument('-f', '--file', help="values in a yaml file")
    helm_deploy_parser.add_argument('-s', '--secure', help="secure", default='', dest='secure')
    helm_deploy_parser.add_argument('-n', '--namespace', help="namespace", default='', dest='namespace')
    helm_deploy_parser.add_argument('-p', '--path', help="chart path", default='', dest='chart_path')
    helm_deploy_parser.add_argument('-d', '--dryRun', help="dry run", action='store_true')
    helm_deploy_parser.add_argument('-v', '--values', help="additional values", default='', dest='values')
    helm_deploy_parser.set_defaults(func=_helm_deploy)

    helm_delete_parser = helm_parser.add_parser('delete')
    helm_delete_parser.add_argument('release_name', help="release name")
    helm_delete_parser.set_defaults(func=_helm_delete)

    if len(sys.argv) == 2 and 'helm' == sys.argv[1]:
        parser.print_help()
        sys.exit()

    if len(sys.argv) == 3 and 'helm' == sys.argv[1] and 'list' == sys.argv[2]:
        helm_list_parser.print_help()
        sys.exit()

    if len(sys.argv) == 3 and 'helm' == sys.argv[1] and 'status' == sys.argv[2]:
        helm_status_parser.print_help()
        sys.exit()

    if len(sys.argv) == 3 and 'helm' == sys.argv[1] and 'deploy' == sys.argv[2]:
        helm_deploy_parser.print_help()
        sys.exit()

    if len(sys.argv) == 3 and 'helm' == sys.argv[1] and 'delete' == sys.argv[2]:
        helm_delete_parser.print_help()
        sys.exit()


def register(parser):
    helm_parser = parser.add_parser('helm')
    _register_arg_options(helm_parser)
