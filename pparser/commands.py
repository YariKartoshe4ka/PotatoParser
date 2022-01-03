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
    """Similar to the **REM** command in Basic and other languages, lines
    beginning with **REM** will not be processed. **REM** is a comment

    :syntax: *REM <comment>*
    :param comment: Comment string
    :example:

    ::

        REM This is a comment!
    """
    pass


class DELAY(DuckyCommand):
    """Command creates a momentary pause in the ducky script. It is quite handy
    for creating a moment of pause between sequential commands that may take
    the target computer some time to process. Multiple **DELAY** commands can
    be used to create longer delays

    :syntax: *DELAY <time>*
    :param time: Time to pause in milliseconds :math:`\\in [1, 10^5]`
    :example:

    ::

        DELAY 5000
        REM I just waited 5 seconds!
    """

    def _parse_arg(self):
        try:
            arg = int(self.arg)
            assert 1 <= arg <= 10000
        except (TypeError, ValueError, AssertionError):
            raise CommandArgumentError('expected integer in range from 1 to 10^5')

        return arg

    def _exec(self, arg):
        return [f'delay({arg});']


class DEFAULTDELAY(DELAY, DuckyCommand):
    """**DEFAULTDELAY** or **DEFAULT_DELAY** is used to define how long to wait
    between each subsequent command. Command must be issued at the beginning of
    the ducky script and is optional. Not specifying the command will result in
    faster execution of ducky scripts. This command is mostly useful when
    debugging

    :syntax: - *DEFAULTDELAY <time>*
             - *DEFAULT_DELAY <time>*
    :param time: Time to pause in milliseconds :math:`\\in [1, 10^5]`
    :example:

    ::

        DEFAULTDELAY 500
        DELAY 750
        DELAY 750
        REM The total pause is 2 seconds
    """

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


class DEFAULT_DELAY(DEFAULTDELAY, DuckyCommand):
    pass


class REPEAT(DuckyCommand):
    """Repeats the last command several times

    :syntax: *REPEAT <num>*
    :param num: Number of repetitions
    :example:

    ::

        DELAY 500
        REPEAT 5
        REM The total pause is 3 seconds

    .. note::

        1. Command cannot be called at the beginning of the script, because it
           will not be able to repeat any command
        2. Command cannot repeat several types of commands: :class:`REM`,
           :class:`DEFAULTDELAY`, :class:`DEFAULT_DELAY`, :class:`REPEAT`
        3. Delay will not be called per repeat if the :class:`DEFAULTDELAY`
           or :class:`DEFAULT_DELAY` was called at the beginning of the file
    """

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
    """Processes the text in two modes (you can choose one)

    1. ALT (each character is entered as an ALT code)
    2. non-ALT (entered as a normal keystroke, only characters which
       supported on a specific keyboard layout

    :syntax: *STRING <string>*
    :param string: Text to print
    :example:

    ::

        STRING Hello World!
        STRING Another text :)
    """

    def _parse_arg(self):
        self.payloads = [printDefaultString]

        if self.arg is None:
            raise CommandArgumentError('expected string, but got nothing')

        arg = str(self.arg)

        if self._pparser.args.disable_alt:
            return arg

        for i, c in enumerate(arg):
            if c not in self._pparser.alphabet:
                raise CommandArgumentError(f'undefined character of string `{c}` in {i + 1} position')

        self.payloads = [printAltString]

        return arg

    def _exec(self, arg):
        if self._pparser.args.disable_alt:
            return [f'printDefaultString(F("{arg}"));']
        return [f"printAltString({{{', '.join(str(self._pparser.alphabet[c]) + '_S' for c in arg)}}});"]


class STRINGDELAY(DuckyCommand):
    """Processes the text in two modes (you can choose one) with a certain
    speed characters typing

    1. ALT (each character is entered as an ALT code)
    2. non-ALT (entered as a normal keystroke, only characters which
       supported on a specific keyboard layout

    :syntax: - *STRINGDELAY <time> <string>*
             - *STRING_DELAY <time> <string>*

    :param time: Time to pause per character in milliseconds :math:`\\in [1, 10^5]`
    :param string: Text to print
    :example:

    ::

        STRINGDELAY 200 Hello World!
        STRING_DELAY 300 Another text
        REM These commands takes 6 seconds!
    """

    def _parse_arg(self):
        self.payloads = [printDefaultString]

        if self.arg is None:
            raise CommandArgumentError('expected 2 arguments, but got nothing')

        args = self.arg.split(' ', 1)

        if len(args) < 2:
            raise CommandArgumentError(f'expected 2 arguments, but got {len(args)}')

        try:
            args[0] = int(args[0])
            assert 1 <= args[0] <= 10000
        except (TypeError, ValueError, AssertionError):
            raise CommandArgumentError('first argument expected as integer in range from 1 to 10^5')

        if self._pparser.args.disable_alt:
            return args

        for i, c in enumerate(args[1]):
            if c not in self._pparser.alphabet:
                raise CommandArgumentError(f'undefined character of string `{c}` in {i + 1} position')

        self.payloads = [printAltString]

        return args

    def _exec(self, arg):
        if self._pparser.args.disable_alt:
            return [f'printDefaultString(F("{arg[1]}"), {arg[0]});']
        return [f"printAltString({{{', '.join(str(self._pparser.alphabet[c]) + '_S' for c in arg[1])}}}, {arg[0]});"]


class STRING_DELAY(STRINGDELAY, DuckyCommand):
    pass


single_keys = {
    'MENU':         'KEY_MENU',
    'APP':          'KEY_MENU',
    'DOWNARROW':    'KEY_DOWN_ARROW',
    'DOWN':         'KEY_DOWN_ARROW',
    'UPARROW':      'KEY_UP_ARROW',
    'UP':           'KEY_UP_ARROW',
    'LEFTARROW':    'KEY_LEFT_ARROW',
    'LEFT':         'KEY_LEFT_ARROW',
    'RIGHTARROW':   'KEY_RIGHT_ARROW',
    'RIGHT':        'KEY_RIGHT_ARROW',
    'DELETE':       'KEY_DELETE',
    'END':          'KEY_END',
    'HOME':         'KEY_HOME',
    'INSERT':       'KEY_INSERT',
    'PAGEUP':       'KEY_PAGE_UP',
    'PAGEDOWN':     'KEY_PAGE_DOWN',
    'PRINTSCREEN':  'KEY_PRINT_SCREEN',
    'PRINTSCRN':    'KEY_PRINT_SCREEN',
    'PRNTSCRN':     'KEY_PRINT_SCREEN',
    'PRTSCN':       'KEY_PRINT_SCREEN',
    'PRSC':         'KEY_PRINT_SCREEN',
    'PRTSCR':       'KEY_PRINT_SCREEN',
    'BREAK':        'KEY_PAUSE',
    'PAUSE':        'KEY_PAUSE',
    'NUMLOCK':      'KEY_NUM_LOCK',
    'CAPSLOCK':     'KEY_CAPS_LOCK',
    'SCROLLLOCK':   'KEY_SCROLL_LOCK',
    'ESC':          'KEY_ESC',
    'ESCAPE':       'KEY_ESC',
    'SPACE':        '\' \'',
    'TAB':          'KEY_TAB',
    'BACKSPACE':    'KEY_BACKSPACE',
    'BKSP':         'KEY_BACKSPACE',
    'ENTER':        'KEY_RETURN',
    'F1':           'KEY_F1',
    'F2':           'KEY_F2',
    'F3':           'KEY_F3',
    'F4':           'KEY_F4',
    'F5':           'KEY_F5',
    'F6':           'KEY_F6',
    'F7':           'KEY_F7',
    'F8':           'KEY_F8',
    'F9':           'KEY_F9',
    'F10':          'KEY_F10',
    'F11':          'KEY_F11',
    'F12':          'KEY_F12',
    'F13':          'KEY_F13',
    'F14':          'KEY_F14',
    'F15':          'KEY_F15',
    'F16':          'KEY_F16',
    'F17':          'KEY_F17',
    'F18':          'KEY_F18',
    'F19':          'KEY_F19',
    'F20':          'KEY_F20',
    'F21':          'KEY_F21',
    'F22':          'KEY_F22',
    'F23':          'KEY_F23',
    'F24':          'KEY_F24',
}


class SingleKey(DuckyCommand):
    payloads = [pressSingleKey]
    key = ''

    def _parse_arg(self):
        if self.arg is not None:
            raise CommandArgumentError("command doesn't accept any arguments")

    def _exec(self, arg):
        return [f'pressSingleKey({self.key});']


for name, key in single_keys.items():
    locals()[name] = type(name, (SingleKey, DuckyCommand), {'key': key})
