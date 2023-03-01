from bokeh.models import ColumnDataSource

from TP4.modules.base.base_plot import BasePlot


class BaseScatterPlot(BasePlot):
    """
    Class implementation of the ScatterPlot primitive
    """

    def __init__(
        self,
        title,
        tools,
        x_axis_label="",
        y_axis_label="",
        tooltips="",
        height=600,
        width=1200,
        **params
    ):
        """
        Constructor of the ScatterPlot
        :param x_axis_label: str
            x axis label
        :param y_axis_label: str
            y axis label
        :param title: str
            plot title
        :param tools: list
            tools to be used by the plot
        :param tooltips: str, optional
            tooltips to be used by the HoverTool
        :param height: int
            plot height
        :param width: int
            plot width
        :param params: inherited args
        """
        super().__init__(**params)
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.title = title
        self.tools = tools
        self.tooltips = tooltips
        self.height = height
        self.width = width
        self.source = ColumnDataSource(data=dict(x=[], y=[], size=[], color=[]))
