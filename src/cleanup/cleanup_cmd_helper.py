from src.lib.process import execute_on_shell, execute

CLEANUP_CMD_STACK = []


class CleanupCommandHelper:

    @staticmethod
    def clean(args):
        if args.intellij:
            execute(CleanupCommandHelper.find_exec_cmd('.idea'))
            execute(CleanupCommandHelper.find_exec_cmd('*.iml'))

        if args.npm:
            execute(CleanupCommandHelper.find_exec_cmd('node_modules'))
            execute(CleanupCommandHelper.find_exec_cmd('package-lock.json'))
            execute(CleanupCommandHelper.find_exec_cmd('yarn.lock'))

        if args.artifacts:
            execute(CleanupCommandHelper.find_exec_cmd('venv'))
            execute(CleanupCommandHelper.find_exec_cmd('target'))
            execute(CleanupCommandHelper.find_exec_cmd('dist'))
            execute(CleanupCommandHelper.find_exec_cmd('artifacts'))

        if args.docker:
            docker_ps_ids = '$(docker ps -aq)'
            execute_on_shell(f'docker update --restart=no {docker_ps_ids} && docker stop {docker_ps_ids}')
            execute_on_shell('docker system prune -f')
            execute_on_shell('docker volume prune -f')

    @staticmethod
    def find_exec_cmd(value) -> []:
        return ['find', './', '-name', value, '-exec', 'rm', '-rf', '{}', ';']
