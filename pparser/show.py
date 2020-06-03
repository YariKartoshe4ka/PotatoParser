from colorama import init, Fore, Style


class Show:

    def __init__(self, stdout):
        init()
        self.stdout = stdout

    def info(self, text):
        print(f'{Style.BRIGHT}{Fore.GREEN}[*]{Style.RESET_ALL} {text}')

    def error(self, text):
        print(f'{Style.BRIGHT}{Fore.RED}[!]{Style.RESET_ALL} {text}')

    def write(self, text):
        self.stdout.write(f'{text}\n')

    def start(self):
        self.stdout.write('#include <Keyboard.h>\n\n/*\nParsed by PotatoParser\nhttps://gihub.com/YariKartoshe4ka/PotatoParser/\n*/\n\nvoid setup() {\n  // Start Keyboard\n  Keyboard.begin();\n\n  // Start payload\n')

    def end(self):
        self.stdout.write('  // End payload\n}\n\n// Unused\nvoid loop() {}')

    def close(self):
        self.stdout.close()
