import sys
from argparse import ArgumentParser

from src.docker.docker_cmd_helper import DockerCommandHelper as Docker, DOCKER_CMD_STACK
from src.lib import process


@Docker.images
def _docker_images(args):
    process.command(DOCKER_CMD_STACK)


@Docker.build
def _docker_build(args):
    process.execute(DOCKER_CMD_STACK)


@Docker.push
def _docker_push(args):
    process.execute(DOCKER_CMD_STACK)


def _docker_build_push(args):
    command = DOCKER_CMD_STACK.copy()

    _docker_build(args)

    DOCKER_CMD_STACK.clear()
    DOCKER_CMD_STACK.extend(command)

    _docker_push(args)


@Docker.login
def _docker_login(args):
    process.execute(DOCKER_CMD_STACK)


def _register_arg_options(parser: ArgumentParser):
    docker_parser = parser.add_subparsers()

    docker_images_parser = docker_parser.add_parser('images')
    docker_images_parser.add_argument('-s', '--search', help="search for image", type=str, default='', dest='search')
    docker_images_parser.set_defaults(func=_docker_images)

    docker_build_parser = docker_parser.add_parser('build')
    docker_build_parser.add_argument('-f', '--file', help="docker file", type=str, default='', dest='file')
    docker_build_parser.add_argument('-t', '--tag', help="image tag [:version]", type=str, default='', dest='tag')
    docker_build_parser.add_argument('-p', '--public', help="use public registry", action='store_true')
    docker_build_parser.set_defaults(func=_docker_build)

    docker_push_parser = docker_parser.add_parser('push')
    docker_push_parser.add_argument('-t', '--tag', help="image tag [:version]", type=str, default='', dest='tag')
    docker_push_parser.add_argument('-p', '--public', help="use public registry", action='store_true')
    docker_push_parser.set_defaults(func=_docker_push)

    docker_bpush_parser = docker_parser.add_parser('bpush')
    docker_bpush_parser.add_argument('-f', '--file', help="docker file", type=str, default='', dest='file')
    docker_bpush_parser.add_argument('-t', '--tag', help="image tag [:version]", type=str, default='', dest='tag')
    docker_bpush_parser.add_argument('-p', '--public', help="use public registry", action='store_true')
    docker_bpush_parser.set_defaults(func=_docker_build_push)

    docker_login_parser = docker_parser.add_parser('login')
    docker_login_parser.add_argument('-i', '--internal', help="internal", action='store_true')
    docker_login_parser.set_defaults(func=_docker_login)

    if len(sys.argv) == 2 and 'docker' == sys.argv[1]:
        parser.print_help()
        sys.exit()


def register(parser):
    docker_parser = parser.add_parser('docker')
    _register_arg_options(docker_parser)
