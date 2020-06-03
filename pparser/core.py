from sys import argv
from os import getcwd
import datetime
from .show import Show
from .pparser import PParser


def entry_point():
    show = Show(open(f'{getcwd()}/sketch.ino', 'w'))

    if len(argv) < 2:
        show.art()
    else:
        path = argv[1]

        start = datetime.datetime.now()

        try:
            parser = PParser(open(path, 'r'), show)
        except FileNotFoundError:
            show.error(f'File {path} not found!')
        else:

            show.start()
            parser.start()
            show.end()

            stop = datetime.datetime.now()
            delta = (stop - start).total_seconds()
            show.info(f'Parsed {parser.count} lines in {delta}s')

    show.close()



if __name__ == '__main__':
    entry_point()
