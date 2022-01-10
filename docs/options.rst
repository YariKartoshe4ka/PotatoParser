Parser options
~~~~~~~~~~~~~~

The parser has several modes and options, which are described below. 


Special buns
============

As mentioned earlier, the main *special* task of this parser is the generation of Arduino sketches from Ducky scripts, taking into account the fact that the victim keyboard layout is still unknown. To accomplish this task, I used the idea of Alt codes. Unfortunately this method is only suitable for Windows OS (I am sure that Linux users won't insert unknown objects into their computer, *lmao*), but I also added normal mode which can be enabled with `--disable-alt`_ option


Command-line options
====================

Here the parser parameters are described in a little more detail

usage:
    *pparser [-h] [-e] [-q] [-o OUTPUT] [-i INDENT] [-a ALPHABET | --disable-alt] SOURCE*

positional arguments:
    SOURCE
        Path to source of ducky script that needs to be parsed

optional arguments:
    -h, --help
        Show this help message and exit, *nothing interesting*

    -e, --error-ok 
        Do not exit if an error occurred during parsing. By default, the parser
        stops working at the first syntax error (if it fails, the sketch file
        remains empty). This behavior can just be changed using this option. After
        the error, the parser will continue its execution and save the sketch in
        any case, while error messages will still be output to the console

    -q, --quiet
        Quiet mode that disables ASCII banner. This option will disable the banner
        and it may slightly speed up parsing (art output takes ~100 ms)

    -o OUTPUT
        Name or path to output directory, contains sketch. If there is no specified
        directory, it will be created. Inside it will be a sketch with the same name
        as the directory, but with the *.ino* extension. Directory defaults to **sketch**

    -i INDENT
        Number of spaces per indent in the output sketch. In principle, it serves only
        for the beauty of the output sketch, but it can also slightly reduce the size
        of the sketch on the disk (about 100 bytes). Defaults to **2**

    -a ALPHABET
        Path to additional alphabets of Alt codes. The option can be specified several
        times for each dictionary separately. The dictionary is written in JSON format.
        Abstractly , the dictionary looks like this:

        .. code-block::

            {
                "key_1": altcode_1,
                "key_2": altcode_2,
                ...
                "key_N": altcode_N
            }

        Examples of dictionaries can be found on
        `GitHub <https://github.com/YariKartoshe4ka/PotatoParser/tree/master/pparser/alphabets>`_.
        ASCII and Russian alphabets are already defined. The option is incompatible with `--disable-alt`_

    .. _`--disable-alt`:

    --disable-alt
        Don't parse strings to Alt codes sequences. As mentioned earlier, the option
        may be useful if victim OS is different from Windows. Disables parsing of
        strings into a sequence of Alt codes, as a result, the string *"Hello World"*
        with the Russian layout will be printed as *"Руддщ Цщкдв"* (transliterated)
        which is no good. Use it at your discretion
