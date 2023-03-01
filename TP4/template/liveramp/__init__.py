"""
Vanilla template
"""
import pathlib

import param
from panel.layout import Card
from panel.template.base import BasicTemplate
from panel.template.theme import DarkTheme, DefaultTheme


class LiverampTemplate(BasicTemplate):
    """
    VanillaTemplate is built on top of Vanilla web components.
    """

    _css = [pathlib.Path(__file__).parent / 'liveramp.css',
            pathlib.Path(__file__).parent / 'liveramp_bokeh.css']

    _template = pathlib.Path(__file__).parent / 'liveramp.html'

    _modifiers = {
        Card: {
            'children': {'margin': (10, 10)},
            'margin': (5, 5)
        }
    }

    def _apply_root(self, name, model, tags):
        if 'main' in tags:
            model.margin = (10, 15, 10, 10)


class LiverampDefaultTheme(DefaultTheme):

    css = param.Filename(default=pathlib.Path(__file__).parent / 'default.css')

    _template = LiverampTemplate


class LiverampDarkTheme(DarkTheme):

    _template = LiverampTemplate
