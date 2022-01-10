Ducky commands
~~~~~~~~~~~~~~

*Ducky Script syntax is simple. Each command resides on a new line and may have options follow. Commands are written in ALL CAPS, because ducks are loud and like to quack with pride. Most commands invoke keystrokes, key-combos or strings of text, while some offer delays or pauses. Below is a list of commands and their function, followed by some example usage.* `[1] <https://docs.hak5.org/hc/en-us/articles/360010555153-Ducky-Script-the-USB-Rubber-Ducky-language>`_

The syntax is very simple and abstractly looks like this:

::

    COMMAND_1 ARGUMENT_1 ARGUMENT_2 ... ARGUMENT_N
    COMMAND_2 ARGUMENT_1 ARGUMENT_2 ... ARGUMENT_N
    ...
    COMMAND_N ARGUMENT_1 ARGUMENT_2 ... ARGUMENT_N

Syntax features
===============

As already mentioned, each command is written from a new line. Empty lines are allowed both at the beginning and end of the file, and between commands (they do not affect the process in any way, the parser simply ignores them)

There must be strictly **one space** between the command and the argument and between each argument. Spaces at the end of lines are truncated, so the command ``"STRING Hello World  "`` will be equivalent to ``"STRING Hello World"``

All commands which supported by the parser are described here


REM
===

.. autoclass:: pparser.commands.REM


DELAY
=====

.. autoclass:: pparser.commands.DELAY


DEFAULTDELAY & DEFAULT_DELAY
==============================

.. autoclass:: pparser.commands.DEFAULTDELAY


REPEAT
======

.. autoclass:: pparser.commands.REPEAT


STRING
======

.. autoclass:: pparser.commands.STRING


STRINGDELAY & STRING_DELAY
==========================

.. autoclass:: pparser.commands.STRINGDELAY


Single Key
==========

.. autoclass:: pparser.commands.SingleKey


Combo Key
=========

.. autoclass:: pparser.commands.ComboKey
