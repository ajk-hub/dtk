import os
import pty
import shlex
import subprocess

from src.lib.common import log_error


def execute(cmd: []):
    try:
        def read(fd):
            data = os.read(fd, 1024)
            return data

        pty.spawn(cmd, read)
    except Exception as e:
        log_error(str(e))


def command(cmd: []):
    execute_on_shell(shlex.join(cmd).replace("'", ""))


def execute_on_shell(cmd: str):
    try:
        subprocess.run(cmd, shell=True)
    except Exception as e:
        log_error(str(e))


if __name__ == '__main__':
    execute(['git', 'log'])
