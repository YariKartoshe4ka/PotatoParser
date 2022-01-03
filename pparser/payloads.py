class Payload:
    text = []
    depends = []


class pressSingleKey(Payload):
    text = [
        'void pressSingleKey(uint8_t key) {',
        [
            'Keyboard.press(key);',
            'delay(20);',
            'Keyboard.release(key);'
        ],
        '}'
    ]


class printAltString(Payload):
    depends = [pressSingleKey]

    text = [
        'uint16_t operator ""_S(unsigned long long x) {',
        [
            'return (uint16_t)x;'
        ],
        '}',
        '',
        'template <size_t N> void printAltString(const uint16_t (&codes)[N], int delayTec = 0) {',
        [
            'for (int code : codes) {',
            [
                'int d = 1;',
                'while (d <= code / 10) d *= 10;',
                'Keyboard.press(KEY_LEFT_ALT);',
                'for (int i = d; i > 0; i /= 10) {',
                [
                    'byte k = (code / i % 10 == 0 ? 234 : code / i % 10 + 224);',
                    'pressSingleKey(k);',
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
    depends = [pressSingleKey]

    text = [
        'void printDefaultString(String string, int delayTec = 0) {',
        [
            'for (char c : string) {',
            [
                'pressSingleKey(c);',
                'delay(delayTec);'
            ],
            '}'
        ],
        '}'
    ]
