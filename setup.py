from setuptools import setup
from pparser import __version__

setup(
    name='pparser',
    version=__version__,
    author='YariKartoshe4ka',
    author_email='yaroslav.kikel.06@inbox.ru',
    packages=['pparser'],
    install_requires=['colorama'],
    entry_points={
        'console_scripts': [
            'pparser=pparser.core:entry_point'
        ]
    },
    license='GNU GPLv3',
    description='Parser from Ducky Script to Ardunio',
    long_description='https://github.com/YariKartoshe4ka/PotatoParser/blob/master/README.md',

    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)