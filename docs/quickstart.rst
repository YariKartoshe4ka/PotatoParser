Quickstart
~~~~~~~~~~

This quickstart will show you all process of conversion Ducky Script to Arduino sketch


Requirements
============

To reproduce what is described here, you need to satisfy the following dependencies

- `Python <https://www.python.org/downloads/>`_
- `Arduino IDE <https://www.arduino.cc/en/software>`_
- `Sublime Text <https://www.sublimetext.com/download>`_

download and install them to continue


Installation
============

Now you can install `PotatoParser <https://www.python.org/downloads/>`_ from PyPI packages using pip

.. code-block:: bash

    pip install pparser

or the latest (but possibly unstable) from GitHub

.. code-block:: bash

    pip install git+https://github.com/YariKartoshe4ka/PotatoParser.git


Processing
==========

Let's write a test ducky script like this

.. code-block::

    REM Opens notepad and writing "Hello World!" 5 times
    WINDOWS r
    DELAY 200
    STRING notepad.exe
    ENTER
    DELAY 500
    STRING Hello World!
    REPEAT 4

And save it as *test.ducky* file. Now you can convert this script to valid Arduino sketch with the following command

.. code-block:: bash

    pparser test.ducky

In current directory you can discover new folder *sketch* which contains Arduino sketch


Flashing
========

Open prepared sketch in Arduino IDE. Connect your board to PC and flash it. Upon completion, the script will start executing and, if you did everything correctly, you will see "Hello World!" printed 10 times in notepad
