from src.config.ci_config import get_ci_config, CIConfig
from src.config.user_preference import get_user_preference, UserPreference
from src.lib.common import git_commit_sha

DOCKER_CMD_STACK = ['docker']


class DockerCommandHelper:
    @staticmethod
    def images(func):
        def executor(args):
            DOCKER_CMD_STACK.append('images')

            if args.search:
                DOCKER_CMD_STACK.append("|")
                DOCKER_CMD_STACK.append('grep')
                DOCKER_CMD_STACK.append(args.search)

            func(args)

        return executor

    @staticmethod
    def build(func):
        def executor(args):
            commit_sha = git_commit_sha()
            ci_config: CIConfig = get_ci_config()
            user_preference: UserPreference = get_user_preference()

            DOCKER_CMD_STACK.append('build')

            DOCKER_CMD_STACK.append('-t')
            if args.tag:
                DOCKER_CMD_STACK.append(args.tag)

            elif args.public:
                DOCKER_CMD_STACK.append(ci_config.DIR_CHART + ':' + commit_sha)

            else:
                DOCKER_CMD_STACK.append(
                    user_preference.internal_image_prefix + ci_config.DIR_CHART + ':' + commit_sha)

            DOCKER_CMD_STACK.append('-f')
            if args.file:
                DOCKER_CMD_STACK.append(args.file)
            else:
                DOCKER_CMD_STACK.append(ci_config.DIR_DOCKER + '/Dockerfile')

            DOCKER_CMD_STACK.append('--build-arg')
            DOCKER_CMD_STACK.append('version=' + commit_sha)

            DOCKER_CMD_STACK.append('.')
            func(args)

        return executor

    @staticmethod
    def push(func):
        def executor(args):
            commit_sha = git_commit_sha()
            ci_config: CIConfig = get_ci_config()
            user_preference: UserPreference = get_user_preference()

            DOCKER_CMD_STACK.append('push')

            if args.tag:
                DOCKER_CMD_STACK.append(args.tag)

            elif args.public:
                DOCKER_CMD_STACK.append(ci_config.DIR_CHART + ':' + commit_sha)

            else:
                DOCKER_CMD_STACK.append(
                    user_preference.internal_image_prefix + ci_config.DIR_CHART + ':' + commit_sha)

            func(args)

        return executor

    @staticmethod
    def login(func):
        def executor(args):
            user_preference: UserPreference = get_user_preference()

            DOCKER_CMD_STACK.append('login')

            if args.internal:
                DOCKER_CMD_STACK.append('-u')
                DOCKER_CMD_STACK.append(user_preference.internal_user)
                DOCKER_CMD_STACK.append('-p')
                DOCKER_CMD_STACK.append(user_preference.internal_pass)
                DOCKER_CMD_STACK.append(user_preference.internal_url)
            else:
                DOCKER_CMD_STACK.append('-u')
                DOCKER_CMD_STACK.append(user_preference.docker_user)
                DOCKER_CMD_STACK.append('-p')
                DOCKER_CMD_STACK.append(user_preference.docker_pass)

            func(args)

        return executor
