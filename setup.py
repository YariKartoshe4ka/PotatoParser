from setuptools import setup, find_packages
from pparser import __version__


# Adding requirements
install_requires = []
with open('requirements.txt', 'r') as file:
    for line in file:
        install_requires.append(line)


setup(
    name='pparser',
    version=__version__,

    author='YariKartoshe4ka',
    author_email='yaroslav.kikel.06@inbox.ru',

    url='https://github.com/YariKartoshe4ka/PotatoParser',

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'pparser=pparser.main:main'
        ]
    },

    include_package_data=True,

    description='Parser from Ducky Script to Ardunio',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    install_requires=install_requires,

    classifiers=[
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Software Development :: Code Generators',
        'Operating System :: OS Independent'
    ]
)
