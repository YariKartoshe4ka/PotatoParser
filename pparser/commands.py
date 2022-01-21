"""File with implementations of Ducky Script language commands
"""

from .exceptions import *
from .payloads import *


class DuckyCommand:
    """Abstract class of Ducky commands. Service commands (which cannot be
    called from a script) have names in the CamelCase style, and work
    commands have the CAPSLOCK style

    Args:
        arg (Union[str, None]): Command argument, what follows after calling the
            command (separated by a space)
        pparser (pparser.parser.PotatoParser): Instance of PotatoParser
    """

    payloads = []

    def __init__(self, arg, pparser):
        self.arg = arg
        self._pparser = pparser

    def exec(self):
        """This method is called when executing the command, doesn't
        change it during inheritance

        Returns:
            list: Generated Arduino code

        Raises:
            CommandArgumentError: Invalid command argument, see argument type
                and description in documentation
            CommandUsageError: Invalid command usage, see usage examples in
                documentation
            CommandInfoWarning: Command skipped due to reason in error description
        """
        return self._exec(self._parse_arg())

    def repeat_exec(self):
        """This method is called when the command is executed again, doesn't
        change it during inheritance

        Returns:
            list: Generated Arduino code

        Raises:
            CommandArgumentError: Invalid command argument, see argument type
                and description in documentation
            CommandUsageError: Invalid command usage, see usage examples in
                documentation
            CommandInfoWarning: Command skipped due to reason in error description
        """
        return self._repeat_exec(self._parse_arg())

    def _parse_arg(self):
        """Responsible for parsing the string following the command call into
        ready-to-use arguments. You can access the string via :attr:`self.arg`

        Returns:
            any: Already parsed argument, return type consistent
            with :meth:`_exec` and :meth:`_repeat_exec`

        Raises:
            CommandArgumentError: Invalid command argument, see argument type
                and description in documentation
        """
        return None

    def _exec(self, arg):
        """Processing the argument and returning the corresponding Arduino code

        Args:
            arg (any): Already parsed argument (via :meth:`_parse_arg`)

        Returns:
            list: Generated Arduino code

        Raises:
            CommandUsageError: Invalid command usage, see usage examples in
                documentation
            CommandInfoWarning: Command skipped due to reason in error description
        """
        return []

    def _repeat_exec(self, arg):
        """Processing the argument again and returning the corresponding
        Arduino code

        Args:
            arg (any): Already parsed argument (via :meth:`_parse_arg`)

        Returns:
            list: Generated Arduino code

        Raises:
            CommandUsageError: Invalid command usage, see usage examples in
                documentation
            CommandInfoWarning: Command skipped due to reason in error description
        """
        return []


class UndefinedCommand(DuckyCommand):
    """Inserted into the processed_commands list when command has
    undefined name
    """

    def _parse_arg(self):
        """Unidentified command is non-working command
        """
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
    debugging. :class:`DELAY` command will override this delay

    :syntax: - *DEFAULTDELAY <time>*
             - *DEFAULT_DELAY <time>*
    :param time: Time to pause in milliseconds :math:`\\in [1, 10^5]`
    :example:

    ::

        DEFAULTDELAY 500
        STRING Super text
        STRING Another super text
        DELAY 300
        STRING Text after delay
        REM The total pause is 1.8 seconds
    """

    def _exec(self, arg):
        if self._pparser.processed_commands:
            raise CommandUsageError('command can be used once at the top of script')

        return []

    def _repeat_exec(self, arg):
        skip_commands = (REM, DEFAULT_DELAY, DEFAULTDELAY, DELAY)

        for skip_command in skip_commands:
            if isinstance(self._pparser.processed_commands[-1], skip_command):
                return []

        return super()._exec(arg)


class DEFAULT_DELAY(DEFAULTDELAY, DuckyCommand):
    pass


class REPEAT(DuckyCommand):
    """Repeats the last *N* commands several times

    :syntax: *REPEAT <num> <amount?>*
    :param num: Number of repetitions
    :param amount: Amount of commands to repeat, defaults to 1
    :example:

    ::

        DELAY 200
        DELAY 500
        REPEAT 5 2
        REM The total pause is 4.2 seconds

    Note:
        1. Command cannot be called if the declared amount of commands to
           repeat is greater than the number of commands already processed
        2. Command cannot repeat several types of commands: :class:`REM`,
           :class:`DEFAULTDELAY`, :class:`DEFAULT_DELAY`, :class:`REPEAT`
        3. Delay will not be called per repeat if the :class:`DEFAULTDELAY`
           or :class:`DEFAULT_DELAY` was called at the beginning of the file
    """

    def _parse_arg(self):
        if self.arg is None:
            raise CommandArgumentError('expected 1 or 2 arguments, but got nothing')

        args = self.arg.split()
        if len(args) > 2:
            raise CommandArgumentError(f'expected 1 or 2 arguments, but got {len(args)}')

        try:
            args[0] = int(args[0])
            assert 1 <= args[0] <= 100
        except (TypeError, ValueError, AssertionError):
            raise CommandArgumentError('first argument expected as integer in range from 1 to 100')

        if len(args) == 2:
            try:
                args[1] = int(args[1])
                assert 1 <= args[1] <= 100
            except (TypeError, ValueError, AssertionError):
                raise CommandArgumentError('second argument expected as integer in range from 1 to 100')
        else:
            args.append(1)

        return args

    def _exec(self, arg):
        prev_commands = self._pparser.processed_commands[-arg[1]:]

        if len(prev_commands) < arg[1]:
            raise CommandArgumentError(f'there are not enough commands to repeat {len(prev_commands)} < {arg[1]}')

        invalid_commands = (REM, DEFAULT_DELAY, DEFAULTDELAY, REPEAT)

        for invalid_command in invalid_commands:
            for prev_command in prev_commands:
                if isinstance(prev_command, invalid_command):
                    raise CommandArgumentError(f'cannot repeat the `{invalid_command.__name__}` command')

        try:
            return [
                f'for (short i = 0; i < {arg[0]}; ++i) {{',
                *[prev_command.exec() for prev_command in prev_commands],
                '}'
            ]
        except Exception:
            raise CommandInfoWarning('Command skipped due to inoperability of previous ones')


class STRING(DuckyCommand):
    """Processes the text in two modes (you can choose one)

    1. Alt (each character is entered as an Alt code)
    2. non-Alt (entered as a normal keystroke, only characters which
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

    1. Alt (each character is entered as an Alt code)
    2. non-Alt (entered as a normal keystroke, only characters which
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
in the following format

.. code-block:: python

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
    """Emulates one special key by one-time pressing. The list of available
    keys and their description are below

    :syntax: *<key>*
    :param key: Key to emulate
    :example:

    ::

        STRING Hello World!
        HOME
        REM I moved to the beginning of the line!

    .. csv-table:: Supported Single Keys
        :header: "Key", "Description"
        :widths: 15, 30

"""

    for k, v in single_keys.items():
        __doc__ += ' ' * 8 + f'"{" or ".join(k)}", "{v[1]}"\n'

    payloads = [pressSingleKey]
    _key = ''

    def _parse_arg(self):
        if self.arg is not None:
            raise CommandArgumentError("command doesn't accept any arguments")

    def _exec(self, arg):
        return [f'pressSingleKey({self._key});']


for names, key_and_desc in single_keys.items():
    key, desc = key_and_desc
    for name in names:
        locals()[name] = type(name, (SingleKey, DuckyCommand), {'_key': key})


"""Available keys for :class:`ComboKey` defined in `combo_keys`
in the following format

.. code-block:: python

    combo_keys = {
        ('KEY_1', 'ALIAS_1_KEY_1', ..., 'ALIAS_N_KEY_1'): ('CONST_KEY_1', 'KEY_1_DESCRIPTION'),
        ('KEY_2', 'ALIAS_1_KEY_2', ..., 'ALIAS_N_KEY_2'): ('CONST_KEY_2', 'KEY_2_DESCRIPTION'),
         ...
        ('KEY_N', 'ALIAS_1_KEY_N', ..., 'ALIAS_N_KEY_N'): ('CONST_KEY_N', 'KEY_N_DESCRIPTION')
    }
"""
combo_keys = {
    ('WINDOWS', 'WIN', 'GUI', 'COMMAND', 'CMD', 'META'): ('KEY_LEFT_GUI', 'Emulates the Windows-Key, sometimes referred to as the Super-key'),
    ('SHIFT',): ('KEY_LEFT_SHIFT', 'Emulates SHIFT key, which can be used when navigating fields to select text, among other functions'),
    ('ALT',): ('KEY_LEFT_ALT', 'Emulates ALT key, which can be used for many functions, such as navigating among windows'),
    ('CONTROL', 'CTRL'): ('KEY_LEFT_CTRL', 'Emulates CONTROL key for very popular combinations: saving a file, undoing the last action, etc.')
}


class ComboKey(DuckyCommand):
    """Emulates key sequences by holding down each key at the same time.
    The list of available combo keys and their description are below

    :syntax: *<key1> <key2?> <key3>*
    :param key1: Main combo key, beginning of the sequence
    :param key2: Optional second combo key, must not match the first one
    :param key3: :class:`SingleKey` or ASCII lowercase character (a-z)
    :example:

    ::

        CONTROL ALT DELETE
        REM Opens auxiliary window

    .. csv-table:: Supported Combo Keys
        :header: "Key", "Description"
        :widths: 15, 30

"""

    for k, v in combo_keys.items():
        __doc__ += ' ' * 8 + f'"{" or ".join(k)}", "{v[1]}"\n'

    payloads = [pressComboKey]
    _key = ''

    def _parse_arg(self):
        if self.arg is None:
            raise CommandArgumentError('expected 1 or 2 arguments, but got nothing')

        args = self.arg.split()
        if len(args) > 2:
            raise CommandArgumentError(f'expected 1 or 2 arguments, but got {len(args)}')

        if len(args) == 2:
            if args[0] == self._key:
                raise CommandArgumentError(f'first argument must not match the command name')

            for names, key_and_desc in combo_keys.items():
                key, _ = key_and_desc
                if args[0] in names:
                    args[0] = key
                    break
            else:
                raise CommandArgumentError(f'first argument expected as ComboKey, but got `{args[0]}`')

        for names, key_and_desc in single_keys.items():
            key, _ = key_and_desc
            if args[-1] in names:
                args[-1] = key
                return args

        if 97 <= ord(args[-1]) <= 122:
            args[-1] = f"'{args[-1]}'"
            return args

        raise CommandArgumentError(f'last argument expected as SingleKey or ASCII lowercase char (a-z), but got `{args[-1]}`')

    def _exec(self, arg):
        return [f"pressComboKey({{{', '.join(['(uint8_t)' + i for i in [self._key] + arg])}}});"]


for names, key_and_desc in combo_keys.items():
    key, desc = key_and_desc
    for name in names:
        locals()[name] = type(name, (ComboKey, DuckyCommand), {'_key': key})
