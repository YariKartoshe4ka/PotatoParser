from os import getcwd, system
from os.path import exists
from colorama import init, Style, Fore


def main():
    if not exists(f'{getcwd()}/PParser.py'):
        print(f'{Style.BRIGT}{Fore.RED}[!]{Style.RESET_ALL} Cannot find main PParser.py file!')
    else:
        system('python3 PParser.py tests/in.txt')

        out = open('tests/out.txt', 'r').read()
        sketch = open('sketch.ino', 'r').read()

        print('=================================')

        if out != sketch:
            print(f'{Style.BRIGHT}{Fore.RED}[!]{Style.RESET_ALL} Test not passed!')
        else:
            print(f'{Style.BRIGHT}{Fore.GREEN}[*]{Style.RESET_ALL} Test passed')


if __name__ == '__main__':
    init()
    main()
