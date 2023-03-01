import panel as pn
import param
from bokeh.models import ColumnDataSource

from TP4.modules.panel_text import PanelText


class BasePlot(param.Parameterized):
    """
    This is a class implementation of a simple BarPlot client
    """

    source = param.ClassSelector(class_=ColumnDataSource)

    def __init__(self, **params):
        """
        Constructor method, initialize the source data
        """
        super().__init__(**params)

    def get_panel(self):
        """
        Get the dashboard inside the panel template
        """
        if len(self.title) > 0:
            panel = pn.Column(
                PanelText(text="## " + self.title).panel, self.figure, sizing_mode="stretch_both"
            )
        else:
            panel = pn.Column(self.figure, sizing_mode="stretch_both")
        return panel
