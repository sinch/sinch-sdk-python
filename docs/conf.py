import os
import sys

# Allow autodoc to import the sinch package from the project root
sys.path.insert(0, os.path.abspath(".."))
from sinch import __version__

# -- Project information -------------------------------------------------------

project = "Sinch Python SDK"
copyright = "2024, Sinch Developer Experience Team"
author = "Sinch Developer Experience Team"
release = __version__

# -- General configuration -----------------------------------------------------

extensions = [
    # Automatically generates .rst files from Python source (replaces running
    # sphinx-apidoc manually — configured via apidoc_modules below)
    "sphinx.ext.apidoc",
    # Pulls docstrings from Python source into the generated .rst files
    "sphinx.ext.autodoc",
    # Adds [source] links that open the highlighted source file
    "sphinx.ext.viewcode",
]

# -- sphinx.ext.apidoc ---------------------------------------------------------
# Runs apidoc automatically during the build — no need for a separate command.
# Each entry in the list corresponds to one package to document.

apidoc_modules = [
    {
        # Path to the Python package, relative to this conf.py file
        "path": "../sinch",
        # Output directory for the generated .rst files, relative to the docs source dir
        "destination": "api",
    }
]

# -- sphinx.ext.autodoc --------------------------------------------------------

autodoc_default_options = {
    # Document all public members (methods, attributes, nested classes)
    "members": True,
    # Show the class inheritance chain
    "show-inheritance": True,
    # Preserve the order in which members appear in the source file
    "member-order": "bysource",
}

# Render type hints as part of the parameter/return descriptions, not the signature
autodoc_typehints = "both"

# -- HTML output ---------------------------------------------------------------

html_theme = "sphinx_rtd_theme"

html_theme_options = {
    # Maximum depth of the navigation sidebar (-1 = unlimited)
    "navigation_depth": -1,
    # Keep all navigation entries expanded by default
    "collapse_navigation": False,
}