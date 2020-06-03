from sys import argv
from os import getcwd
import datetime
from .show import Show
from .pparser import PParser


#################################################

def entry_point(path):
    start = datetime.datetime.now()

    show = Show(open(f'{getcwd()}/sketch.ino', 'w'))

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
    entry_point(argv[1])