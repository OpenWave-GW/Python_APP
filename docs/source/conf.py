# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'mpo_api'
copyright = '2024, GW Instek'
author = 'GW Instek'
release = '1.0.0'

# -- General configuration
import os
import sys
sys.path.insert(0, os.path.abspath('../../lib'))

autodoc_mock_imports=[
'dso_usb',
'lvgl',
]

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']
autodoc_preserve_defaults = True

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Options for EPUB output
#epub_show_urls = 'footnote'
