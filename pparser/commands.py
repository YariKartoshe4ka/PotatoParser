from .exceptions import *
from .payloads import *


class DuckyCommand:
    payloads = []

    def __init__(self, arg, pparser):
        self.arg = arg
        self._pparser = pparser

    def exec(self) -> list:
        return self._exec(self._parse_arg())

    def repeat_exec(self) -> list:
        return self._repeat_exec(self._parse_arg())

    def _parse_arg(self) -> any:
        return None

    def _exec(self, arg) -> list:
        return []

    def _repeat_exec(self, arg) -> list:
        return []


class UndefinedCommand(DuckyCommand):
    def _parse_arg(self):
        raise Exception


class REM(DuckyCommand):
    pass


class DELAY(DuckyCommand):
    def _parse_arg(self):
        try:
            arg = int(self.arg)
            assert 1 <= arg <= 10000
        except (TypeError, ValueError, AssertionError):
            raise CommandArgumentError('expected integer in range from 1 to 10^5')

        return arg

    def _exec(self, arg):
        return [f'delay({arg});']


class DEFAULT_DELAY(DELAY, DuckyCommand):
    def _exec(self, arg):
        if self._pparser.processed_commands:
            raise CommandUsageError('command can be used once at the top of script')

        return []

    def _repeat_exec(self, arg):
        skip_commands = (REM, DEFAULT_DELAY, DEFAULTDELAY)

        for skip_command in skip_commands:
            if isinstance(self._pparser.processed_commands[-1], skip_command):
                return []

        return super()._exec(arg)


class DEFAULTDELAY(DEFAULT_DELAY, DuckyCommand):
    pass


class ENTER(DuckyCommand):
    def _parse_arg(self):
        if self.arg is not None:
            raise CommandArgumentError("command doesn't accept any arguments")

    def _exec(self, arg):
        return ['Keyboard.press(KEY_RETURN); Keyboard.release(KEY_RETURN);']


class REPEAT(DuckyCommand):
    def _parse_arg(self):
        try:
            arg = int(self.arg)
            assert 1 <= arg <= 100
        except (TypeError, ValueError, AssertionError):
            raise CommandArgumentError('expected integer in range from 1 to 100')

        return arg

    def _exec(self, arg):
        if not self._pparser.processed_commands:
            raise CommandUsageError('command cannot be used in the top of script')

        prev_command = self._pparser.processed_commands[-1]
        invalid_commands = (REM, DEFAULT_DELAY, DEFAULTDELAY, REPEAT)

        for invalid_command in invalid_commands:
            if isinstance(prev_command, invalid_command):
                raise CommandArgumentError(f'cannot repeat the `{invalid_command.__name__}` command')

        try:
            return [
                f'for (short i = 0; i < {arg}; ++i) {{',
                prev_command.exec(),
                '}'
            ]
        except Exception:
            raise CommandInfoError('Command skipped due to inoperability of previous')


class STRING(DuckyCommand):
    def _parse_arg(self):
        if self.arg is None:
            raise CommandArgumentError('expected string, got nothing')

        arg = str(self.arg)

        if self._pparser.args.disable_alt:
            return arg

        self.payloads.append(print_alt_string)

        for i, c in enumerate(arg):
            if c not in self._pparser.alphabet:
                raise CommandArgumentError(f'undefined character of string `{c}` in {i + 1} position')

        return arg

    def _exec(self, arg):
        if self._pparser.args.disable_alt:
            return [f'Keyboard.print("{arg}");']
        return [f"print_alt_string({{{', '.join(str(self._pparser.alphabet[c]) + '_S' for c in arg)}}});"]
