import sys
from argparse import ArgumentParser

from src.cleanup import entrypoint as cleanup
from src.docker import entrypoint as docker
from src.helm import entrypoint as helm
from src.k6 import entrypoint as k6
from src.maven import entrypoint as maven


def get_arg_parser() -> ArgumentParser:
    return ArgumentParser(prog='dtk', description='Development Tool Kit')


def load_arg_parser():
    parser = get_arg_parser()
    sub_parser = parser.add_subparsers(title='tools')

    maven.register(sub_parser)
    docker.register(sub_parser)
    helm.register(sub_parser)
    k6.register(sub_parser)
    cleanup.register(sub_parser)

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    else:
        args.func(args)
