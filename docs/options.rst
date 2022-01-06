Parser options
~~~~~~~~~~~~~~

usage:
    *pparser [-h] [-e] [-q] [-o OUTPUT] [-i INDENT] [-a ALPHABET | --disable-alt] SOURCE*

positional arguments:
    SOURCE
        Path to source of ducky script that needs to be parsed

optional arguments:
    -h, --help      show this help message and exit
    -e, --error-ok  Do not exit if an error occurred during parsing
    -q, --quiet     Quiet mode that disables ASCII banner
    -o OUTPUT       Name or path to output directory, contains sketch
    -i INDENT       Number of spaces per indent in the output sketch
    -a ALPHABET     Path to additional alphabets of Alt codes
    --disable-alt   Don't parse strings to Alt codes sequences
