import sys
from argparse import ArgumentParser

from src.lib import process
from src.maven.maven_cmd_helper import MAVEN_CMD_STACK
from src.maven.maven_cmd_helper import MavenCommandHelper as Maven


@Maven.clean
def _mvn_clean(args):
    process.execute(MAVEN_CMD_STACK)


@Maven.install
def _mvn_install(args):
    process.execute(MAVEN_CMD_STACK)


@Maven.deploy
def _mvn_deploy(args):
    process.execute(MAVEN_CMD_STACK)


def _mvn_sonar(args):
    if args.test:
        args.skipTest = False
        args.module = None
        _mvn_install(args)

    Maven.sonar(args)
    process.execute(MAVEN_CMD_STACK)


def _register_arg_options(parser: ArgumentParser):
    mvn_parser = parser.add_subparsers()

    mvn_clean_parser = mvn_parser.add_parser('clean')
    mvn_clean_parser.set_defaults(func=_mvn_clean)

    mvn_install_parser = mvn_parser.add_parser('install')
    mvn_install_parser.add_argument('-m', '--module', help="module", default='', dest='module')
    mvn_install_parser.add_argument('-s', '--skipTest', help="skip test", action='store_true')
    mvn_install_parser.set_defaults(func=_mvn_install)

    mvn_deploy_parser = mvn_parser.add_parser('deploy')
    mvn_deploy_parser.add_argument('-s', '--skipTest', help="skip test", action='store_true')
    mvn_deploy_parser.set_defaults(func=_mvn_deploy)

    mvn_sonar_parser = mvn_parser.add_parser('sonar')
    mvn_sonar_parser.add_argument('-t', '--test', help="run test", action='store_true')
    mvn_sonar_parser.add_argument('-s', '--server', help="server", default='', dest='server')
    mvn_sonar_parser.add_argument('-u', '--username', help="username", default='', dest='username')
    mvn_sonar_parser.add_argument('-p', '--password', help="password", default='', dest='password')
    mvn_sonar_parser.set_defaults(func=_mvn_sonar)

    if len(sys.argv) == 2 and 'maven' == sys.argv[1]:
        parser.print_help()
        sys.exit()


def register(parser):
    maven_parser = parser.add_parser('maven')
    _register_arg_options(maven_parser)
