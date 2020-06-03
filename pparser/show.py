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

    def art(self):
        print(f'''{Style.BRIGHT}{Fore.GREEN}   _____        _          _          _____                              
  |  __ \\      | |        | |        |  __ \\                             
  | |__) |___  | |_  __ _ | |_  ___  | |__) |__ _  _ __  ___   ___  _ __ 
  |  ___// _ \\ | __|/ _` || __|/ _ \\ |  ___// _` || '__|/ __| / _ \\| '__|
  | |   | (_) || |_| (_| || |_| (_) || |   | (_| || |   \\__ \\|  __/| |   
  |_|    \\___/  \\__|\\__,_| \\__|\\___/ |_|    \\__,_||_|   |___/ \\___||_|{Style.RESET_ALL}
  
  Github: https://github.com/YariKartoshe4ka/PotatoParser/
  PYPI: https://pypi.org/project/pparser/

  {Style.BRIGHT}{Fore.RED}Using: pparser <path_to_your_ducky_script_file>{Style.RESET_ALL}\n''')

    def close(self):
        self.stdout.close()
