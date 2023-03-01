import numpy as np
from bokeh.models import ColumnDataSource, HoverTool, LabelSet, Span
from bokeh.plotting import figure

from TP4.modules.base.base_plot import BasePlot


class ScatterPlot(BasePlot):
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


class VersusScatterPlot(ScatterPlot):
    """
    Class implementation of the VersusScatterPlot primitive
    """

    def __init__(self, **params):
        """
        Constructor of the VersusScatterPlot
        :param params: inherited args
        """
        super().__init__(**params)

        if len(self.tooltips) > 0:
            self.hover = HoverTool(tooltips=self.tooltips)
            self.tools = [self.hover] + self.tools

        self.source = ColumnDataSource(
            data=dict(x=[], y=[], size=[], color=[], categories=[], sorted_x=[], fit_x=[])
        )

        self.make_figure()
        self.panel = self.get_panel()

    def init_best_fit_line(self, x, y):
        """
        At each refresh, update the best fit line wrt the updated data
        :param x: list
            x values
        :param y: list
            y values
        """
        # determine best fit line (polyfit of degree 3)
        z = np.polyfit(x, y, 3)
        fit = np.poly1d(z)
        self.source.data["sorted_x"] = np.sort(x)
        self.source.data["fit_x"] = fit(np.sort(x))

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        # Create plot
        self.figure = figure(
            tools=self.tools, plot_width=self.width, plot_height=self.height, title=""
        )
        self.figure.scatter(x="x", y="y", size="size", color="color", source=self.source)

        # name of the x-axis
        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label

        # Labels
        labels = LabelSet(
            x="x",
            y="y",
            text="categories",
            x_offset=5,
            y_offset=5,
            text_font_size="6pt",
            source=self.source,
        )
        self.figure.add_layout(labels)

        # Horizontal & vertical line
        vline = Span(
            location=100,
            dimension="height",
            line_color="black",
            line_width=1,
            line_dash="dashed",
            level="underlay",
        )
        hline = Span(
            location=100,
            dimension="width",
            line_color="black",
            line_width=1,
            line_dash="dashed",
            level="underlay",
        )
        self.figure.renderers.extend([vline, hline])

        self.figure.line(
            x="sorted_x", y="fit_x", line_width=1, line_dash="dashed", source=self.source
        )

        # bissectrice
        self.figure.line(
            x="sorted_x",
            y="fit_x",
            line_color="darkgray",
            line_width=1,
            line_dash="dashed",
            source=self.source,
        )

        self.figure.toolbar.logo = None
