from distutils.core import setup
from pparser import __version__

setup(
    name='pparser',
    version=__version__,
    author='YariKartoshe4ka',
    author_email='yaroslav.kikel.06@inbox.ru',
    packages=['pparser'],
    entry_points={
        'console_scripts': [
            'pparser=pparser.core:entry_point'
        ]
    },
    license='GNU GPLv2',
    description='Parser from Ducky Script to Ardunio',

    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)