from argparse import ArgumentParser
from pathlib import Path
from time import time

from colorama import init

from .parser import PotatoParser
from .art import gen_art


def main():
    init()

    parser = ArgumentParser(description='Potato Parser')

    parser.add_argument(dest='source', type=Path, metavar='SOURCE', help='Path to source of ducky script that needs to be parsed')

    parser.add_argument('-e', '--error-ok', action='store_true', help='Do not exit if an error occurred during parsing')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode that disables ASCII banner')
    parser.add_argument('-i', dest='indent', type=int, metavar='INDENT', default=2, help='Number of spaces per indent in the output sketch')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', dest='alphabets', type=Path, metavar='ALPHABET', action='append', help='Path to additional alphabets of ALT codes ', default=[])
    group.add_argument('--disable-alt', action='store_true', help='Don\'t parse strings to ALT codes sequences')

    args = parser.parse_args()

    if not args.quiet:
        print(gen_art())

    start = time()
    pparser = PotatoParser(args)

    with open(args.source, encoding='utf-8') as source:
        for line in source:
            pparser.exec(*line.rstrip().split(' ', 1))
            pparser.i += 1

    pparser.sketch.flush()
    pparser.log_success(f'Successfully parsed {pparser.i} lines in {round((time() - start) * 1000)}ms')
