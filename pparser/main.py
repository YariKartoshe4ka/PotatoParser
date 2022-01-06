"""File containing the main parser entrypoint
"""

from argparse import ArgumentParser
from pathlib import Path
from time import time
from sys import argv

from .parser import PotatoParser
from .art import gen_art


def main(argv=argv[1:]):
    """Main entrypoint of PotatoParser

    Args:
        argv (Optional[list]): Parser options, defaults to `sys.argv`
    """

    parser = ArgumentParser(description='Potato Parser is converter of Ducky Script to Arduino sketch with some additional funcitons (like Alt codes)')

    parser.add_argument(dest='source', type=Path, metavar='SOURCE', help='path to source of ducky script that needs to be parsed')

    parser.add_argument('-e', '--error-ok', action='store_true', help='do not exit if an error occurred during parsing')
    parser.add_argument('-q', '--quiet', action='store_true', help='quiet mode that disables ASCII banner')
    parser.add_argument('-o', dest='output', type=str, metavar='OUTPUT', default='sketch', help='name or path to output directory, contains sketch')
    parser.add_argument('-i', dest='indent', type=int, metavar='INDENT', default=2, help='number of spaces per indent in the output sketch')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', dest='alphabets', type=Path, metavar='ALPHABET', action='append', help='path to additional alphabets of Alt codes ', default=[])
    group.add_argument('--disable-alt', action='store_true', help='don\'t parse strings to Alt codes sequences')

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
    pparser.log_success(f'Successfully parsed {pparser.i} line{"s" * bool(pparser.i - 1)} in {round((time() - start) * 1000)}ms')
