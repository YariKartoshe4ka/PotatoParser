"""File contains a function that generates an ASCII banner
"""

from colorama import init, Style, Fore
from packaging.version import parse
from requests import get

from . import __version__


init()


# Define color aliases
C = Style.RESET_ALL + Style.BRIGHT + Fore.CYAN      # Cyan
W = Style.RESET_ALL + Style.BRIGHT + Fore.WHITE     # White
B = Style.RESET_ALL + Style.NORMAL + Fore.YELLOW    # Brown
G = Style.RESET_ALL + Style.DIM + Fore.WHITE        # Gray
Y = Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW    # Yellow
R = Style.RESET_ALL                                 # Reset


def _get_remote_version():
    """Function returns the latest version of the parser published on PyPI.
    Request is limited in time in ~100ms

    Returns:
        str: if there are stable Internet connection it returns the latest
            remote version, otherwise **0.0.0**
    """
    try:
        r = get('https://pypi.org/pypi/pparser/json', timeout=0.1)
        return max(r.json()['releases'], key=lambda x: parse(x))

    except Exception:
        return '0.0.0'


def gen_art():
    """The main function generating the ASCII banner

    Returns:
        str: colored ASCII banner
    """

    # Create art template
    art = '''
                            W/:
                          /:YsWN   /.
                        /:Y++/Wm++o+:
                        +Yo/--:::dW+
                G...+hyh-.W-+Yo:.`.yWhs:
            G``.omhyyyohyysoWoYoo-.-+oW-
            G/dyooB+++++++++GosWyYoo+oW/`        {0}
          G.+ysB+++++++++++G///oWm.:`          {1}
     G-ooosmysyB++++++++++++G//++M-           {2}
   G-sByooGyNyB+CHhB+WyB++WsoB++CHhB++++++GMho-
   GsBhsGyy+msB++++WmdhmyB++++++++GomdBssGyo
   G:+: `MoB+GooB++++++++++++++Goy+ mBshGy
       G`yyoB+++++++++oyGyyyss+`  mBhyG/
        G:dBdhyGssssssyByosGmo.     --`
       G`NBsooGyh`````shB+++Gm/
        Gssoo/`     :yByyGys-
                    G`---`R
'''

    # Coloring the art
    art = art.replace('C', C) \
        .replace('W', W) \
        .replace('B', B) \
        .replace('G', G) \
        .replace('Y', Y) \
        .replace('R', R)

    # Adding dynamic information
    remote_version = _get_remote_version()

    if parse(remote_version) > parse(__version__):
        new_update = f'{C}available ({remote_version})'
    else:
        new_update = f'{W}unavailable'

    return art.format(
        f'{Y}PotatoParser{W} by YariKartoshe4ka{R}',
        f'{Y}Current version:{W} {__version__}{R}',
        f"{Y}New update: {new_update}{R}"
    )
