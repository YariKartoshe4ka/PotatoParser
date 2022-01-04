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


"""Available keys for :class:`SingleKey` defined in `single_keys`
in the following format::

    single_keys = {
        ('KEY_1', 'ALIAS_1_KEY_1', ..., 'ALIAS_N_KEY_1'): ('CONST_KEY_1', 'KEY_1_DESCRIPTION'),
        ('KEY_2', 'ALIAS_1_KEY_2', ..., 'ALIAS_N_KEY_2'): ('CONST_KEY_2', 'KEY_2_DESCRIPTION'),
         ...
        ('KEY_N', 'ALIAS_1_KEY_N', ..., 'ALIAS_N_KEY_N'): ('CONST_KEY_N', 'KEY_N_DESCRIPTION')
    }
"""

single_keys = {
    ('MENU', 'APP'): ('KEY_MENU', 'Emulates the App key, sometimes referred to as the menu key or context menu key. On Windows systems this is similar to the SHIFT F10 key combo, producing the menu similar to a right-click'),
    ('DOWNARROW', 'DOWN'): ('KEY_DOWN_ARROW', 'Emulates down arrow key'),
    ('UPARROW', 'UP'): ('KEY_UP_ARROW', 'Emulates down arrow key'),
    ('LEFTARROW', 'LEFT'): ('KEY_LEFT_ARROW', 'Emulates left arrow key'),
    ('RIGHTARROW', 'RIGHT'): ('KEY_RIGHT_ARROW', 'Emulates right arrow key'),
    ('DELETE',): ('KEY_DELETE', 'Emulates delete key'),
    ('END',): ('KEY_END', 'Emulates end key'),
    ('HOME',): ('KEY_HOME', 'Emulates home key'),
    ('INSERT',): ('KEY_INSERT', 'Emulates insert key'),
    ('PAGEUP',): ('KEY_PAGE_UP', 'Emulates page up key'),
    ('PAGEDOWN',): ('KEY_PAGE_DOWN', 'Emulated page down key'),
    ('PRINTSCREEN', 'PRINTSCRN', 'PRNTSCRN', 'PRTSCN', 'PRSC', 'PRTSCR'): ('KEY_PRINT_SCREEN', 'Emulates PrtSc (Print Screen) key, which typically takes screenshots'),
    ('BREAK', 'PAUSE'): ('KEY_PAUSE', 'Emulates Pause/Break key'),
    ('NUMLOCK',): ('KEY_NUM_LOCK', 'Toggle numlock'),
    ('CAPSLOCK',): ('KEY_CAPS_LOCK', 'Toggle capslock'),
    ('SCROLLLOCK',): ('KEY_SCROLL_LOCK', 'Toggle scroll lock'),
    ('ESC', 'ESCAPE'): ('KEY_ESC', 'Emulates esc key'),
    ('SPACE',): ("' '", 'Emulates spacebar'),
    ('TAB',): ('KEY_TAB', 'Emulates tab key'),
    ('BACKSPACE', 'BKSP'): ('KEY_BACKSPACE', 'Emulates backspace key. On MacOS this is the delete key'),
    ('ENTER',): ('KEY_RETURN', 'Emulates enter key'),
    ('F1',): ('KEY_F1', 'Emulates F1 key'),
    ('F2',): ('KEY_F2', 'Emulates F2 key'),
    ('F3',): ('KEY_F3', 'Emulates F3 key'),
    ('F4',): ('KEY_F4', 'Emulates F4 key'),
    ('F5',): ('KEY_F5', 'Emulates F5 key'),
    ('F6',): ('KEY_F6', 'Emulates F6 key'),
    ('F7',): ('KEY_F7', 'Emulates F7 key'),
    ('F8',): ('KEY_F8', 'Emulates F8 key'),
    ('F9',): ('KEY_F9', 'Emulates F9 key'),
    ('F10',): ('KEY_F10', 'Emulates F10 key'),
    ('F11',): ('KEY_F11', 'Emulates F11 key'),
    ('F12',): ('KEY_F12', 'Emulates F12 key'),
    ('F13',): ('KEY_F13', 'Emulates F13 key'),
    ('F14',): ('KEY_F14', 'Emulates F14 key'),
    ('F15',): ('KEY_F15', 'Emulates F15 key'),
    ('F16',): ('KEY_F16', 'Emulates F16 key'),
    ('F17',): ('KEY_F17', 'Emulates F17 key'),
    ('F18',): ('KEY_F18', 'Emulates F18 key'),
    ('F19',): ('KEY_F19', 'Emulates F19 key'),
    ('F20',): ('KEY_F20', 'Emulates F20 key'),
    ('F21',): ('KEY_F21', 'Emulates F21 key'),
    ('F22',): ('KEY_F22', 'Emulates F22 key'),
    ('F23',): ('KEY_F23', 'Emulates F23 key'),
    ('F24',): ('KEY_F24', 'Emulates F24 key'),
}


class SingleKey(DuckyCommand):
    """Emulates one special key. The list of available keys and their
    description are below

    :syntax: *<key>*
    :param key: Key to emulate
    :example:

    ::

        STRING Hello World!
        HOME
        REM I moved to the beginning of the line!

    .. csv-table:: Supported Keys
        :header: "Key", "Description"
        :widths: 15, 30

"""

    for k, v in single_keys.items():
        __doc__ += ' ' * 8 + f'"{" or ".join(k)}", "{v[1]}"\n'

    payloads = [pressSingleKey]
    key = ''

    def _parse_arg(self):
        if self.arg is not None:
            raise CommandArgumentError("command doesn't accept any arguments")

    def _exec(self, arg):
        return [f'pressSingleKey({self.key});']


for names, key_and_desc in single_keys.items():
    key, desc = key_and_desc
    for name in names:
        locals()[name] = type(name, (SingleKey, DuckyCommand), {'key': key})
