from src.config.user_preference import get_user_preference, UserPreference

HELM_CMD_STACK = ['helm']


class HelmCommandHelper:
    @staticmethod
    def list(func):
        def executor(args):
            HELM_CMD_STACK.append('list')

            func(args)

        return executor

    @staticmethod
    def status(func):
        def executor(args):
            HELM_CMD_STACK.append('status')

            if args.debug:
                HELM_CMD_STACK.append('--debug')

            if args.desc:
                HELM_CMD_STACK.append('--show-desc')

            HELM_CMD_STACK.append(args.release_name)
            func(args)

        return executor

    @staticmethod
    def deploy(func):
        def executor(args):
            user_preference: UserPreference = get_user_preference()
            namespace = args.namespace if args.namespace else user_preference.helm_default_namespace
            chart_path = args.chart_path if args.chart_path else user_preference.helm_default_chart_path

            HELM_CMD_STACK.append('upgrade')
            HELM_CMD_STACK.append('--install')
            HELM_CMD_STACK.append('--wait')
            HELM_CMD_STACK.append('--force')
            HELM_CMD_STACK.append('--timeout=900s')
            HELM_CMD_STACK.append('--namespace=' + namespace)

            if args.dryRun:
                HELM_CMD_STACK.append("--dry-run")
                HELM_CMD_STACK.append('--debug')

            if args.file:
                HELM_CMD_STACK.append('-f')
                HELM_CMD_STACK.append(chart_path + '/' + args.file)

            if args.secure:
                HELM_CMD_STACK.append("--set")
                HELM_CMD_STACK.append("keycloak.deploy=true")
                HELM_CMD_STACK.append("--set")
                HELM_CMD_STACK.append(
                    f"global.keycloak.VirtualService.host={args.secure}-secure.{user_preference.base_domain}")

            if args.values:
                values = str(args.values).split(",")
                for value in values:
                    fields = value.split(":")

                    if len(fields) > 1:
                        HELM_CMD_STACK.append("--set")
                        HELM_CMD_STACK.append(f"{fields[0]}.deploy=true,{fields[0]}.image.tag={fields[1]}")

                    elif len(fields) == 1:
                        HELM_CMD_STACK.append("--set")
                        HELM_CMD_STACK.append(f"{fields[0]}.deploy=true")

            HELM_CMD_STACK.append(args.release_name)
            HELM_CMD_STACK.append("./" + chart_path)

            func(args)

        return executor

    @staticmethod
    def delete(func):
        def executor(args):
            HELM_CMD_STACK.append('del')
            HELM_CMD_STACK.append(args.release_name)

            func(args)

        return executor
