PotatoParser
======

PotatoParser is a Python script for parsing Ducky Script to Arduino.



Required Tools
--------------

* `Python3`: PotatoParser is compatible only with `python3`.
* [`Colorama`](https://pypi.org/project/colorama/): For pretty text in bash


Install PotatoParser
--------------
To install onto your computer run:

```bash
git clone https://github.com/YariKartoshe4ka/PotatoParser.git
cd PotatoParser
pip3 install -r requirements.txt
python3 setup.py install
```
or install with pip:
```bash
sudo pip3 install pparser
```


Run PotatoParser
----------
```

pparser script.ducky
```
In work derictory will be generated sketch.ino file, which contain complete Arduino code


Testing
----------
```
python3 tests/runtest.py
```
If the last line is equal, the test is passed, otherwise the test is not passed



**Note:** Uninstalling is [not as easy](https://stackoverflow.com/questions/1550226/python-setup-py-uninstall#1550235). The only way to uninstall is to record the files installed by the above command and *remove* those files:

```bash
sudo python3 setup.py install --record files.txt \
  && cat files.txt | xargs sudo rm \
  && rm -f files.txt
```

**Warning!** Some commands are not implemented!
