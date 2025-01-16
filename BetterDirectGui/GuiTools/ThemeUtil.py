"""Tools to work with themes."""
from copy import deepcopy
from typing import Any
from panda3d.core import Filename
import os
import sys

# some useful directories for assets
root = Filename.fromOsSpecific(os.path.dirname(os.path.dirname(__file__)))
if getattr(sys, "frozen", False):
    root = "BetterDirectGui"

assets = f"{root}/assets"
dark = f"{assets}/dark"
light = f"{assets}/light"


def merge(theme1: dict[str: dict[str: Any]] = None, theme2: dict[str: dict[str: Any]] = None) -> dict[str: dict[str: Any]]:
    """Return a new theme that is based on theme1 and updated with the values from theme2."""
    new_theme = deepcopy(theme1)
    if new_theme is None:
        new_theme = {}

    if theme2 is None:
        return new_theme

    for key, value in theme2.items():
        if key in new_theme:
            new_theme[key].update(value)
        else:
            new_theme[key] = value

    return new_theme


def create_theme_from_gui(widget, general_options=None) -> dict[str: dict[str: Any]]:
    """Take the options set by the user on the widget and make a theme based on it.
        Use 'general_options' to fill the 'general' field of the theme."""
    new_theme = {type(widget).__name__: deepcopy(widget._kw)}
    if general_options is not None:
        new_theme["general"] = general_options

    return new_theme


def create_theme_from_guis(widgets: list, general_options=None) -> dict[str: dict[str: Any]]:
    """Take the options set by the user on the widgets and make a theme based on it.
        Use 'general_options' to fill the 'general' field of the theme."""
    new_theme = {}
    for widget in widgets:
        new_theme[type(widget).__name__] = deepcopy(widget._kw)

    if general_options is not None:
        new_theme["general"] = general_options

    return new_theme
