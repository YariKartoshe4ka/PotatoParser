from json import load
from pathlib import Path
from sys import exit

from colorama import init, Style, Fore

from .commands import *
from .exceptions import *
from .sketch import Sketch


init()


class PotatoParser:
    def __init__(self, args):
        self.args = args
        self.sketch = Sketch(args.indent)
        self.i = 0
        self.processed_commands = []

        self.alphabet = {}
        for path in (Path(__file__).parent / 'alphabets').glob('*.json'):
            with open(path, encoding='utf-8') as file:
                self.alphabet.update(load(file))

        for path in args.alphabets:
            with open(path, encoding='utf-8') as file:
                self.alphabet.update(load(file))

    def exec(self, cmd, arg=None):
        if not cmd:
            return

        for command in DuckyCommand.__subclasses__():
            if cmd == command.__name__:
                command = command(arg, self)

                try:
                    out = command.exec()
                except CommandArgumentError as e:
                    self.log_error('Invalid command argument(s)', str(e))
                except CommandUsageError as e:
                    self.log_error('Invalid command usage', str(e))
                except CommandInfoError as e:
                    self.log_info(str(e))
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
        self.log_error('Undefined command', f'`{cmd}`')

    def log_error(self, name, desc):
        print(f'{Style.BRIGHT}{Fore.RED}[!]{Style.RESET_ALL} {name}: {desc} (line {self.i + 1})')

        if self.args.error_ok:
            self.is_success = False
        else:
            exit()

    def log_info(self, msg):
        print(f'{Style.BRIGHT}{Fore.BLACK}[*] {msg} (line {self.i + 1}){Style.RESET_ALL}')

    def log_success(self, msg):
        print(f'{Style.BRIGHT}{Fore.GREEN}[+]{Style.RESET_ALL} {msg}')
