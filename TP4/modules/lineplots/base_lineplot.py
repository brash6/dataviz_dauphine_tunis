from bokeh.models import ColumnDataSource

from TP4.modules.base.base_plot import BasePlot


class LinePlot(BasePlot):
    """
    Class implementation for basic barplot
    """

    def __init__(
            self,
            title,
            x_axis_data=None,
            x_axis_label="",
            y_axis_label="",
            legend_title="",
            legend_label="",
            tooltips="",
            colors="",
            tools="",
            height=600,
            width=1200,
            **params
    ):
        """
        Constructor of a basic barplot
        :param x_axis_data: list
            x axis data used for plot initialization
        :param title: str
            plot title
        :param x_axis_label: str
            x axis label
        :param y_axis_label: str
            y axis label
        :param legend_title: str, optional
            legend title
        :param legend_label: list, optional
            legend labels
        :param tooltips: str
            tooltips used by the HoverTool
        :param colors: list
            colors used by the plot
        :param tools: list
            Bokeh tools to be used by the plot
        :param height: int
            height of the plot
        :param width: int
            width of the plot
        :param params: inherited args
        """
        super().__init__(**params)
        if x_axis_data is None:
            x_axis_data = ["init"]
        self.x_axis_data = x_axis_data
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.tools = tools
        self.title = title
        self.colors = colors
        self.legend_title = legend_title
        self.legend_label = legend_label
        self.tooltips = tooltips
        self.height = height
        self.width = width
        self.source = ColumnDataSource(data=dict(x=[], y=[]))
