from json import load
from pathlib import Path
from sys import exit

from .commands import *
from .exceptions import PotatoParserError, PotatoParserWarning
from .sketch import Sketch
from .utils import *


class PotatoParser:
    def __init__(self, args):
        self.args = args
        self.sketch = Sketch(args.output, args.indent)
        self.i = 0
        self.processed_commands = []

        self.alphabet = {}
        for path in (Path(__file__).parent / 'alphabets').glob('*.json'):
            with open(path, encoding='utf-8') as file:
                self.alphabet.update(load(file))

        for path in args.alphabets:
            check_file(path)
            with open(path, encoding='utf-8') as file:
                self.alphabet.update(load(file))

        # Redefining `_log_func` funcitons of exceptions
        # Not clear method, but working
        PotatoParserError._log_func = self.log_error
        PotatoParserWarning._log_func = self.log_info

    def exec(self, cmd, arg=None):
        if not cmd:
            return

        for command in DuckyCommand.__subclasses__():
            if command.__name__.isupper() and cmd == command.__name__:
                command = command(arg, self)

                try:
                    out = command.exec()
                except (PotatoParserWarning, PotatoParserError) as e:
                    e.log()
                else:
                    self.sketch.add(out, command.payloads)

                self.processed_commands.append(command)

                for processed_command in self.processed_commands:
                    try:
                        self.sketch.add(processed_command.repeat_exec())
                    except Exception:
                        pass

                return

        self.processed_commands.append(UndefinedCommand(arg, self))
        self.log_error(f'Undefined command: `{cmd}`')

    def log_error(self, msg):
        log_error(f'{msg} (line {self.i + 1})')

        if self.args.error_ok:
            self.is_success = False
        else:
            exit(1)

    def log_info(self, msg):
        log_info(f'{msg} (line {self.i + 1})')
