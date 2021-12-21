class Payload:
    text = []
    depends = []


class print_alt_string(Payload):
    text = [
        'unsigned short operator ""_S(unsigned long long x) {',
        [
            'return (unsigned short)x;'
        ],
        '}',
        '',
        'template <size_t N> void print_alt_string(const unsigned short (&codes)[N]) {',
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
                    'Keyboard.release(k);'
                ],
                '}',
                'Keyboard.release(KEY_LEFT_ALT);'
            ],
            '}'
        ],
        '}'
    ]
