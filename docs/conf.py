import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from pparser import __version__


project = 'PotatoParser'
copyright = '2021, YariKartoshe4ka'
author = 'YariKartoshe4ka'

version = __version__
release = __version__

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme'
]


templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'


language = 'en'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


def setup(app):
    app.add_css_file('theme_overrides.css')
