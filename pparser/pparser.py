class PParser:

    def __init__(self, stdin, show):
        self.stdin = stdin
        self.show = show
        self.count = 0

        self.enter = '  Keyboard.press(KEY_RETURN); Keyboard.release(KEY_RETURN);'

        self.translator = {
            'A': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(230); Keyboard.release(230); Keyboard.press(229); Keyboard.release(229); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'B': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(230); Keyboard.release(230); Keyboard.press(230); Keyboard.release(230); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'C': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(230); Keyboard.release(230); Keyboard.press(231); Keyboard.release(231); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'D': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(230); Keyboard.release(230); Keyboard.press(232); Keyboard.release(232); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'E': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(230); Keyboard.release(230); Keyboard.press(233); Keyboard.release(233); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'F': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(231); Keyboard.release(231); Keyboard.press(234); Keyboard.release(234); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'G': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(231); Keyboard.release(231); Keyboard.press(225); Keyboard.release(225); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'H': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(231); Keyboard.release(231); Keyboard.press(226); Keyboard.release(226); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'I': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(231); Keyboard.release(231); Keyboard.press(227); Keyboard.release(227); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'J': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(231); Keyboard.release(231); Keyboard.press(228); Keyboard.release(228); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'K': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(231); Keyboard.release(231); Keyboard.press(229); Keyboard.release(229); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'L': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(231); Keyboard.release(231); Keyboard.press(230); Keyboard.release(230); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'M': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(231); Keyboard.release(231); Keyboard.press(231); Keyboard.release(231); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'N': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(231); Keyboard.release(231); Keyboard.press(232); Keyboard.release(232); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'O': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(231); Keyboard.release(231); Keyboard.press(233); Keyboard.release(233); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'P': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(232); Keyboard.release(232); Keyboard.press(234); Keyboard.release(234); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'Q': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(232); Keyboard.release(232); Keyboard.press(225); Keyboard.release(225); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'R': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(232); Keyboard.release(232); Keyboard.press(226); Keyboard.release(226); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'S': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(232); Keyboard.release(232); Keyboard.press(227); Keyboard.release(227); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'T': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(232); Keyboard.release(232); Keyboard.press(228); Keyboard.release(228); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'U': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(232); Keyboard.release(232); Keyboard.press(229); Keyboard.release(229); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'V': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(232); Keyboard.release(232); Keyboard.press(230); Keyboard.release(230); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'W': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(232); Keyboard.release(232); Keyboard.press(231); Keyboard.release(231); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'X': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(232); Keyboard.release(232); Keyboard.press(232); Keyboard.release(232); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'Y': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(232); Keyboard.release(232); Keyboard.press(233); Keyboard.release(233); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'Z': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(233); Keyboard.release(233); Keyboard.press(234); Keyboard.release(234); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'a': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(233); Keyboard.release(233); Keyboard.press(231); Keyboard.release(231); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'b': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(233); Keyboard.release(233); Keyboard.press(232); Keyboard.release(232); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'c': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(233); Keyboard.release(233); Keyboard.press(233); Keyboard.release(233); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'd': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(234); Keyboard.release(234); Keyboard.press(234); Keyboard.release(234); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'e': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(234); Keyboard.release(234); Keyboard.press(225); Keyboard.release(225); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'f': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(234); Keyboard.release(234); Keyboard.press(226); Keyboard.release(226); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'g': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(234); Keyboard.release(234); Keyboard.press(227); Keyboard.release(227); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'h': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(234); Keyboard.release(234); Keyboard.press(228); Keyboard.release(228); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'i': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(234); Keyboard.release(234); Keyboard.press(229); Keyboard.release(229); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'j': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(234); Keyboard.release(234); Keyboard.press(230); Keyboard.release(230); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'k': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(234); Keyboard.release(234); Keyboard.press(231); Keyboard.release(231); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'l': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(234); Keyboard.release(234); Keyboard.press(232); Keyboard.release(232); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'm': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(234); Keyboard.release(234); Keyboard.press(233); Keyboard.release(233); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'n': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(225); Keyboard.release(225); Keyboard.press(234); Keyboard.release(234); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'o': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(225); Keyboard.release(225); Keyboard.press(225); Keyboard.release(225); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'p': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(225); Keyboard.release(225); Keyboard.press(226); Keyboard.release(226); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'q': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(225); Keyboard.release(225); Keyboard.press(227); Keyboard.release(227); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'r': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(225); Keyboard.release(225); Keyboard.press(228); Keyboard.release(228); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            's': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(225); Keyboard.release(225); Keyboard.press(229); Keyboard.release(229); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            't': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(225); Keyboard.release(225); Keyboard.press(230); Keyboard.release(230); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'u': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(225); Keyboard.release(225); Keyboard.press(231); Keyboard.release(231); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'v': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(225); Keyboard.release(225); Keyboard.press(232); Keyboard.release(232); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'w': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(225); Keyboard.release(225); Keyboard.press(233); Keyboard.release(233); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'x': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(226); Keyboard.release(226); Keyboard.press(234); Keyboard.release(234); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'y': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(226); Keyboard.release(226); Keyboard.press(225); Keyboard.release(225); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            'z': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(226); Keyboard.release(226); Keyboard.press(226); Keyboard.release(226); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            ',': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(228); Keyboard.release(228); Keyboard.press(228); Keyboard.release(228); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            '.': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(228); Keyboard.release(228); Keyboard.press(230); Keyboard.release(230); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            '/': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(228); Keyboard.release(228); Keyboard.press(231); Keyboard.release(231); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            '<': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(230); Keyboard.release(230); Keyboard.press(234); Keyboard.release(234); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            '>': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(230); Keyboard.release(230); Keyboard.press(226); Keyboard.release(226); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            '?': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(230); Keyboard.release(230); Keyboard.press(227); Keyboard.release(227); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            ';': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(229); Keyboard.release(229); Keyboard.press(233); Keyboard.release(233); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            ':': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(229); Keyboard.release(229); Keyboard.press(232); Keyboard.release(232); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            '"': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(227); Keyboard.release(227); Keyboard.press(228); Keyboard.release(228); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            '[': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(233); Keyboard.release(233); Keyboard.press(225); Keyboard.release(225); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            ']': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(233); Keyboard.release(233); Keyboard.press(227); Keyboard.release(227); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            '{': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(226); Keyboard.release(226); Keyboard.press(227); Keyboard.release(227); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            '}': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(225); Keyboard.release(225); Keyboard.press(226); Keyboard.release(226); Keyboard.press(229); Keyboard.release(229); Keyboard.release(KEY_LEFT_ALT); delay(10);',
            ' ': '  Keyboard.press(KEY_LEFT_ALT); Keyboard.press(227); Keyboard.release(227); Keyboard.press(226); Keyboard.release(226); Keyboard.release(KEY_LEFT_ALT); delay(10);',

            'END':    'KEY_END',
            'ESC':    'KEY_ESC',
            'ESCAPE': 'KEY_ESC',
            'F1':     'KEY_F1',
            'F2':     'KEY_F2',
            'F3':     'KEY_F3',
            'F4':     'KEY_F4',
            'F5':     'KEY_F5',
            'F6':     'KEY_F6',
            'F7':     'KEY_F7',
            'F8':     'KEY_F8',
            'F9':     'KEY_F9',
            'F10':    'KEY_F10',
            'F11':    'KEY_F11',
            'F12':    'KEY_F12',
            'SPACE':  ' ',
            'TAB':    'KEY_TAB',

            'DELETE':     'KEY_DELETE',
            'HOME':       'KEY_HOME',
            'INSERT':     'KEY_INSERT',
            'PAGEUP':     'KEY_PAGE_UP',
            'PAGEDOWN':   'KEY_PAGE_DOWN',
            'WINDOWS':    'KEY_LEFT_GUI',
            'GUI':        'KEY_LEFT_GUI',
            'UPARROW':    'KEY_UP_ARROW',
            'DOWNARROW':  ' EY_DOWN_ARROW',
            'LEFTARROW':  'KEY_LEFY_ARROW',
            'RIGHTARROW': 'KEY_RIGHT_ARROW',
        }


    def start(self):
        with self.stdin as file:
            for line in file:
                self.count += 1

                repeat = self.parse(line)
                if repeat:
                    for time in range(repeat):
                        self.parse(previous_line)

                previous_line = line


    def parse(self, line):
        line = line.lstrip().rstrip().split(' ')


        if line[0] == 'REM':
            self.show.write(self.rem(' '.join(line[1:])))

        elif line[0] == 'DELAY':
            self.show.write(self.delay(line[1]))


        elif line[0] == 'STRING':
            self.show.write(self.string(' '.join(line[1:])))


        elif line[0] == 'GUI' or line[0] == 'WINDOWS':
            if len(line[1]) == 1:
                self.show.write(self.gui(line[1]))
            else:
                self.show.error(f'Command {line[0]} using with single char, not with string! (line:{self.count})')


        elif line[0] == 'SHIFT':
            second_button = self.translator.get(line[1], None)
            if second_button:
                self.show.write(self.shift(second_button))
            else:
                self.show.error(f'Command SHIFT take DELETE, HOME, INSERT, PAGEUP, PAGEDOWN, WINDOWS, GUI, UPARROW, DOWNARROW, LEFTARROW, RIGHTARROW, TAB parameter! (line:{self.count})')


        elif line[0] == 'ALT':
            second_button = self.translator.get(line[1], None)
            if len(line[1]) == 1:
                self.show.write(self.alt(f"'{line[1]}'"))
            elif second_button:
                self.show.write(self.alt(second_button))
            else:
                self.show.error(f'Command ALT take END, ESC, ESCAPE, F1...F12, Single Char, SPACE, TAB parameter! (line:{self.count})')


        elif line[0] == 'REPEAT':
            if self.count > 1:
                try:
                    return int(line[1])
                except ValueError:
                    self.show.error(f'Command REPEAT take number of times to repeat, not string! (line:{self.count})')
            else:
                self.show.error(f'You cannot use command REPEAT as a first command! (line:{self.count})')


        elif line[0] == 'ENTER':
            self.show.write(self.enter)


        else:
            self.show.error(f'Command {line[0]} was not recognized! (line:{self.count})')

        return 0




    def rem(self, line):
        return f"\n  // {line}"
    
    def string(self, line):
        out = list()

        for letter in line:
            out.append(self.translator.get(letter, ''))

        return '\n'.join(out)

    def delay(self, time):
        return f'  delay({time});'

    def alt(self, key):
        return f'  Keyboard.press(KEY_LEFT_ALT); Keyboard.press({key}); Keyboard.releaseAll();'

    def gui(self, key):
        return f'  Keyboard.press(KEY_LEFT_GUI); Keyboard.press(\'{key}\'); Keyboard.releaseAll();'

    def shift(self, key):
        return f'  Keyboard.press(KEY_LEFT_SHIFT); Keyboard.press({key}); Keyboard.releaseAll();'
