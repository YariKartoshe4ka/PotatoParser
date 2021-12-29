class Payload:
    text = []
    depends = []


class printAltString(Payload):
    text = [
        'unsigned short operator ""_S(unsigned long long x) {',
        [
            'return (unsigned short)x;'
        ],
        '}',
        '',
        'template <size_t N> void printAltString(const unsigned short (&codes)[N], int delayTec = 0) {',
        [
            'for (int code : codes) {',
            [
                'int d = 1;',
                'while (d <= code / 10) d *= 10;',
                'Keyboard.press(KEY_LEFT_ALT);',
                'for (int i = d; i > 0; i /= 10) {',
                [
                    'byte k = (code / i % 10 == 0 ? 234 : code / i % 10 + 224);',
                    'Keyboard.press(k);',
                    'delay(50);',
                    'Keyboard.release(k);',
                    'delay(delayTec);'
                ],
                '}',
                'Keyboard.release(KEY_LEFT_ALT);'
            ],
            '}'
        ],
        '}'
    ]


class printDefaultString(Payload):
    text = [
        'void printDefaultString(String string, int delayTec = 0) {',
        [
            'for (char c : string) {',
            [
                'Keyboard.print(string);',
                'delay(delayTec);'
            ],
            '}'
        ],
        '}'
    ]
