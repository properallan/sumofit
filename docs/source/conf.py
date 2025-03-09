# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import subprocess

# Obtém a versão do projeto a partir da última tag Git
try:
    release = subprocess.check_output(["git", "describe", "--tags"]).strip().decode("utf-8")
except subprocess.CalledProcessError:
    release = "unknown"  # Caso não haja tags no repositório

# Define a versão do projeto
version = release.split("-")[0]  # Por exemplo, 'v0.1.0' vira 'v0.1'
project = "sumofit"
copyright = '2025, Allan Moreira de Carvalho'
author = 'Allan Moreira de Carvalho'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',   # Para documentação automática a partir das docstrings
    'sphinx.ext.napoleon',  # Para suportar docstrings no estilo Google/NumPy
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


# Para gerar uma tabela de conteúdo
html_use_index = True

# Para gerar a tabela de autores e modificação
html_show_sphinx = False
