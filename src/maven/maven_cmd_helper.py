from src.config.user_preference import get_user_preference, UserPreference

MAVEN_CMD_STACK = ['mvn']


class MavenCommandHelper:

    @staticmethod
    def clean(func):
        def executor(args):
            MavenCommandHelper.append_clean()

            func(args)

        return executor

    @staticmethod
    def install(func):
        def executor(args):
            MavenCommandHelper.append_clean()
            MAVEN_CMD_STACK.append('install')
            MavenCommandHelper.skiptest(args)

            if args.module:
                MAVEN_CMD_STACK.append('-pl')
                MAVEN_CMD_STACK.append(args.module)

            func(args)

        return executor

    @staticmethod
    def deploy(func):
        def executor(args):
            MavenCommandHelper.append_clean()
            MAVEN_CMD_STACK.append('deploy')
            MavenCommandHelper.skiptest(args)

            func(args)

        return executor

    @staticmethod
    def sonar(args):
        user_preference: UserPreference = get_user_preference()

        server = args.server if args.server else user_preference.sonar_url
        username = args.username if args.username else user_preference.sonar_user
        password = args.password if args.password else user_preference.sonar_pass

        MAVEN_CMD_STACK.clear()
        MAVEN_CMD_STACK.append('mvn')
        MAVEN_CMD_STACK.append('sonar:sonar')
        MAVEN_CMD_STACK.append('-Dsonar.host.url=' + server)
        MAVEN_CMD_STACK.append('-Dsonar.login=' + username)
        MAVEN_CMD_STACK.append('-Dsonar.password=' + password)

    @staticmethod
    def append_clean():
        MAVEN_CMD_STACK.append('clean')

    @staticmethod
    def skiptest(args):
        if args.skipTest:
            MAVEN_CMD_STACK.append('-DskipTests')
