"""File containing auxiliary functions
"""

from sys import exit

from colorama import Style, Fore


def log_error(msg):
    """Logs error message to console

    Args:
        msg (str): message to log
    """
    print(f'{Style.BRIGHT}{Fore.RED}[!]{Style.RESET_ALL} {msg}')


def log_info(msg):
    """Logs info message to console

    Args:
        msg (str): message to log
    """
    print(f'{Style.BRIGHT}{Fore.BLACK}[*] {msg}{Style.RESET_ALL}')


def log_success(msg):
    """Logs success message to console

    Args:
        msg (str): message to log
    """
    print(f'{Style.BRIGHT}{Fore.GREEN}[+]{Style.RESET_ALL} {msg}')


def check_file(path):
    """Check whether the path corresponds to the real file. In case
    of failure, writes error message and exits with exit code 1

    Args:
        path (pathlib.Path): path to chech
    """
    if path.exists() and path.is_file():
        return

    log_error(f"File `{path}` doesn't exist")
    exit(1)
