import sys

from src.cleanup.cleanup_cmd_helper import CleanupCommandHelper as Cleanup


def _cleanup(args):
    Cleanup.clean(args)


def register(parser):
    cleanup_parser = parser.add_parser('cleanup')
    cleanup_parser.add_argument('-i', '--intellij', help="intellij", action='store_true')
    cleanup_parser.add_argument('-n', '--npm', help="npm", action='store_true')
    cleanup_parser.add_argument('-a', '--artifacts', help="artifacts", action='store_true')
    cleanup_parser.add_argument('-d', '--docker', help="docker", action='store_true')
    cleanup_parser.set_defaults(func=_cleanup)

    if len(sys.argv) == 2 and 'cleanup' == sys.argv[1]:
        cleanup_parser.print_help()
        sys.exit()
