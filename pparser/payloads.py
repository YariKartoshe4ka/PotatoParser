"""File containing various paylods (C++ sources) responsible for certain
functions and simplifying (or reducing) the final size of the sketch
"""


class Payload:
    """Abstract class for each payload. The arguments are specified
    directly in the class itself

    Args:
        header (str): Multiline or one-line responsible for the function
            declaration is inserted at the top of the sketch, before
            *setup* function
        text (Tuple[Union[Tuple, str]]): Sources of the declared function,
            which are written in a special format described below
        depends (List[Payload]): Paylods required for the current paylod
            to work. An empty list can be passed

    Note:
        The special format of the function sources is as follows: in order
        for paylods to be used with different indentation sizes, nested lists
        are used instead of indents. For example, this C++ code:

        .. code-block:: c++

            void printHelloWorld() {
                Serial.println(F("Hello World"));
            }

        will equivalent to this on Python:

        .. code-block:: python

            text = [
                'void printHelloWorld() {',
                [
                    'Serial.println(F("Hello World"));'
                ],
                '}'
            ]
    """

    depends = []
    header = ''
    text = []


class pressSingleKey(Payload):
    header = 'void pressSingleKey(uint8_t key);'
    text = [
        'void pressSingleKey(uint8_t key) {',
        [
            'Keyboard.press(key);',
            'delay(20);',
            'Keyboard.release(key);'
        ],
        '}'
    ]


class pressComboKey(Payload):
    header = 'template <size_t N> void pressComboKey(const uint8_t (&keys)[N]);'
    text = [
        'template <size_t N> void pressComboKey(const uint8_t (&keys)[N]) {',
        [
            'for (uint8_t key : keys) Keyboard.press(key);',
            'delay(20);',
            'Keyboard.releaseAll();'
        ],
        '}'
    ]


class printAltString(Payload):
    header = '''uint16_t operator ""_S(unsigned long long x);
template <size_t N> void printAltString(const uint16_t (&codes)[N], int delayTec = 0);'''

    depends = [pressSingleKey]

    text = [
        'uint16_t operator ""_S(unsigned long long x) {',
        [
            'return (uint16_t)x;'
        ],
        '}',
        '',
        'template <size_t N> void printAltString(const uint16_t (&codes)[N], int delayTec) {',
        [
            'for (uint16_t code : codes) {',
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
    header = 'void printDefaultString(String string, int delayTec = 0);'
    depends = [pressSingleKey]

    text = [
        'void printDefaultString(String string, int delayTec) {',
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
