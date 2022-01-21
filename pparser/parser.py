"""File containing a class responsible for parsing commands
"""

from json import load
from pathlib import Path
from sys import exit

from .commands import *
from .exceptions import PotatoParserError, PotatoParserWarning
from .sketch import Sketch
from .utils import log_error, log_info, check_file


class PotatoParser:
    """The main class of the parser, which is created in a single instance.
    Directly responsible for parsing commands

    Args:
        args (argparse.Namespace): arguments obtained by :class:`argparse.ArgumentParser`
    """

    def __init__(self, args):
        self.args = args

        # Create `Sketch` instance to control output sketch
        self.sketch = Sketch(args.output, args.indent)

        # Line on which the parser is currently looking
        self.i = 0

        # List of already processed commands (it is necessary to
        # repeat commands such as `DEFAULTDELAY`)
        self.processed_commands = []

        # Generate alphabet dictionary of Alt codes, if they aren't disabled
        if not args.disable_alt:
            self.alphabet = {}

            # First load the alphabets supplied by default...
            for path in (Path(__file__).parent / 'alphabets').glob('*.json'):
                with open(path, encoding='utf-8') as file:
                    self.alphabet.update(load(file))

            # ...then specified by the user
            for path in args.alphabets:
                # Don't forget to check if file is already exists
                check_file(path)

                with open(path, encoding='utf-8') as file:
                    self.alphabet.update(load(file))

        # Redefining `_log_func` funcitons of exceptions
        # Not clear method, but working
        PotatoParserError._log_func = self.log_error
        PotatoParserWarning._log_func = self.log_info

    def exec(self, cmd, arg=None):
        """The method that is called to parse the current line of the script.
        Calling it for each line of the input script will result in its complete
        parsing

        Args:
            cmd (str): current command name (see syntax documentation for more
                details). If current line is blank, **cmd** contains empty string
            arg (Union[str, None]): the arguments of the command or, more simply,
                the string following the name of the command. If the command has
                no arguments specified, **arg** contains ``None``
        """

        # For blank lines
        if not cmd:
            return

        # Find command by iterating through the names of defined commands
        for command in DuckyCommand.__subclasses__():
            if command.__name__.isupper() and cmd == command.__name__:
                # Create an instance of the command
                command = command(arg, self)

                try:
                    # Try to execute the command
                    out = command.exec()
                except (PotatoParserWarning, PotatoParserError) as e:
                    # Logs error, if it's occurred
                    e.log()
                else:
                    # On success add command output to sketch
                    self.sketch.add(out, command.payloads)

                self.processed_commands.append(command)

                # Repeat processed commands
                for processed_command in self.processed_commands:
                    try:
                        self.sketch.add(processed_command.repeat_exec())
                    except Exception:
                        pass

                return

        # The specified command doesn't exist, so we will add `UndefinedCommand`
        # instead of this to `processed_commands`
        self.processed_commands.append(UndefinedCommand(arg, self))
        self.log_error(f'Undefined command: `{cmd}`')

    def log_error(self, msg):
        """Small wrap of the original :func:`log_error` function
        """
        log_error(f'{msg} (line {self.i + 1})')

        if self.args.error_ok:
            self.is_success = False
        else:
            exit(1)

    def log_info(self, msg):
        """Small wrap of the original :func:`log_info` function
        """
        log_info(f'{msg} (line {self.i + 1})')
