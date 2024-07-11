"""
Sphinx configuration file.
"""

# pylint: disable=invalid-name,redefined-builtin

import json
import os
import sys
from typing import Any

from fastapi.openapi.utils import get_openapi
from sphinx.application import Sphinx
from sphinx.ext import apidoc

from jupyterhub_ai_gateway.app import create_app

sys.path.append(os.path.abspath("_pygments/"))


def generate_api_reference(
    *args: Any, **kwargs: Any
):  # pylint: disable=unused-argument
    """
    Generate API reference documentation.

    Parameters:
        *args (Any): Positional arguments.
        **kwargs (Any): Keyword arguments.
    """

    config_dir = os.path.abspath(os.path.dirname(__file__))

    module_path = os.path.join(config_dir, "..", "jupyterhub_ai_gateway/")
    output_path = os.path.join(config_dir, "api-reference/")

    apidoc.main(["-f", "-e", "-T", "-d", "1", "-o", output_path, module_path])


def generate_rest_api_reference(
    *args: Any, **kwargs: Any
):  # pylint: disable=unused-argument
    """
    Generate REST API reference documentation.

    Parameters:
        *args (Any): Positional arguments.
        **kwargs (Any): Keyword arguments.
    """

    config_dir = os.path.abspath(os.path.dirname(__file__))

    test_config_path = os.path.join(
        config_dir, "..", "tests", "data", "test-config.yaml"
    )
    output_path = os.path.join(config_dir, "_static", "openapi.json")

    app = create_app(test_config_path)

    with open(output_path, "w", encoding="utf-8") as file:
        data = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            routes=app.routes,
        )

        json.dump(data, file)


def setup(app: Sphinx):
    """
    Sphinx setup stage.

    Parameters:
        app (Sphinx): Sphinx application instance.
    """

    app.connect("builder-inited", generate_api_reference)
    app.connect("builder-inited", generate_rest_api_reference)


html_title = "JupyterHub AI Gateway"
html_logo = "_static/images/logo.svg"
html_static_path = ["_static/", "_static/images/"]
html_css_files = ["styles/custom.css"]
copyright = "2024, JupyterHub AI Gateway Developers. All rights reserved"

html_theme = "sphinx_book_theme"
html_theme_options = {
    "navigation_with_keys": False,
    "max_navbar_depth": 1,
    "logo": {
        "text": html_title,
    },
    "use_fullscreen_button": False,
    "use_repository_button": True,
    "repository_url": "https://github.com/danilopeixoto/jupyterhub-ai-gateway",
    "icon_links": [
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/jupyterhub-ai-gateway",
            "icon": "fab fa-python",
        },
    ],
    "article_header_end": [
        "navbar-icon-links",
        "article-header-buttons",
    ],
}
html_sidebars = {
    "**": [
        "navbar-logo",
        "search-button-field",
        "sbt-sidebar-nav",
    ],
}

favicons = [
    "favicon.ico",
    {"rel": "apple-touch-icon", "href": "apple-icon.png"},
]

source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_favicon",
    "myst_parser",
]
