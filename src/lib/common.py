import logging
import os
import subprocess
import sys

LOGGER = logging.getLogger()


# ------------------------------------------------
def user_home(filepath: str) -> str:
    return os.path.expanduser(f"~/{filepath}")


# ------------------------------------------------
def expand_path(filepath: str) -> str:
    return os.path.expanduser(filepath)


# ------------------------------------------------
def log_error(message: str):
    LOGGER.critical(f"{message}")
    sys.exit(1)


# ------------------------------------------------
def git_commit_sha() -> str:
    cmd = "git rev-parse HEAD | cut -c 1-8"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    commit_sha = ps.communicate()[0].decode('utf-8').replace('\n', '')

    if commit_sha:
        return commit_sha
    else:
        return 'latest'
