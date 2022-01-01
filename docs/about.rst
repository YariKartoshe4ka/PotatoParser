About PotatoParser
~~~~~~~~~~~~~~~~~~

PotatoParser is a converter from Ducky Script to Arduino sketches


Prehistory
==========

Once, wandering through the Internet, I came across an unusual device - `Rubber Ducky <https://hak5.org/products/usb-rubber-ducky-deluxe>`_ from Hak5, the main function of which was an imitation of the keyboard (`BadUSB <https://en.wikipedia.org/wiki/BadUSB>`_ attack). It cost quite a lot (50$!), so I decided to order a slightly different Rubber Ducky - from Aliexpress. Inside there was a trimmed Arduino Micro SS board. I found only one Ducky Script `converter <https://github.com/thehackingsage/ducky4arduino>`_ to Arduino sketch on the Internet, but I couldn't use it because of problems with the dependent `HID-Keyboard.h <https://github.com/NicoHood/HID>`_ library. As a result, I wrote various scripts with my hands and `found <https://qna.habr.com/q/784003>`_ that the text being printed depends on the current layout of the user's keyboard, and if it is different from English, the whole attack could have failed (I have a Russian one). This prompted me to write my own parser with many additional functions


Advantages
==========

Unfortunately nothing is perfect, just like my parser

Pros
----

- Uses pre-installed `Keyboard.h`_ library at background which eliminates the excruciating problem of installing dependencies
- Parser supports `ALT codes <https://en.wikipedia.org/wiki/Alt_code>`_, thanks to which you can print text regardless of the current victim keyboard layout
- The output sketch is well optimized in memory. This allows you to convert large enough scripts with long texts without fear of overflowing your microcontroller's memory

Cons
----

- I tried to implement almost all the keyboard commands of the original Ducky Script language, but as unnecessary, I omitted the mouse commands
- Unfortunately, the `Keyboard.h`_ library does not support all boards, but only those

    *These core libraries allow the 32u4 and SAMD based boards (Leonardo, Esplora, Zero, Due and MKR Family) to appear as a native Mouse and/or Keyboard to a connected computer* `[1] <https://www.arduino.cc/reference/en/language/functions/usb/keyboard>`_

.. _Keyboard.h: https://github.com/arduino-libraries/Keyboard
