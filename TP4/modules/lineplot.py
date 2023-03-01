import math

from bokeh.models import Circle, ColumnDataSource, FuncTickFormatter, HoverTool, Line
from bokeh.plotting import figure

from TP4.modules.base.base_plot import BasePlot


# Function to format ticks, so that they do not overlap
def x_tick_formatter(plot, num=1):
    """
    This function enables to display ticks so that they do not overlap each other.
    Above 20 ticks, the plot will only display one tick out of int(num_ticks/20)

    Args:
        plot: str
        num: int
            Total number of ticks.
        """

    if num >= 20:
        plot.figure.xaxis.formatter = FuncTickFormatter(code="""
                        var n = Math.trunc(ticks.length/20)
                        if (index % n == 0)
                        {
                        return tick;
                        }
                        else
                        {
                        return "";
                        }
                        """)
    else:
        plot.figure.xaxis.formatter = FuncTickFormatter(code="""
                return tick;
                """)


class LinePlot(BasePlot):
    """
    Class implementation of the MultiLine plot primitive
    """

    def __init__(
            self,
            x_axis_data,
            title,
            tools,
            color,
            line_width,
            size,
            x_axis_label="",
            y_axis_label="",
            tooltips="",
            height=250,
            width=1200,
            **params
    ):
        """
        Constructor of the LinePlot
        :param x_axis_label: str
            x axis label
        :param y_axis_label: str
            y axis label
        :param title: str
            Plot title
        :param tools: list
            tools to be used by the plots
        :param tooltips: str, optional
            tooltips to be used by the HoverTool
        :param params: inherited args
        """
        super().__init__(**params)

        self.x_axis_data = x_axis_data
        self.height = height
        self.width = width
        self.tools = tools
        self.tooltips = tooltips
        # Initialise hover tool
        if len(self.tooltips) > 0:
            self.hover = HoverTool(tooltips=self.tooltips)
            self.tools = [self.hover] + self.tools

        self.color = color
        self.line_width = line_width
        self.size = size

        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.title = title

        self.source = ColumnDataSource(data=dict(x=[], y=[]))

        self.make_figure()
        self.panel = self.get_panel()

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        self.figure = figure(
            x_range=self.x_axis_data,
            tools=self.tools,
            title="",
            height=self.height,
            tooltips=self.tooltips,
            width=self.width
        )
        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label

        self.line = Line(x="x", y="y", line_color=self.color, line_width=self.line_width)

        self.circle = Circle(x="x", y="y", line_color=self.color, fill_color="white", line_width=self.line_width,
                             size=self.size)

        self.figure.add_glyph(self.source, self.line)
        self.figure.add_glyph(self.source, self.circle)

        self.figure.toolbar.logo = None
        self.figure.xaxis.axis_line_color = None
        self.figure.yaxis.axis_line_color = None
        self.figure.xgrid.grid_line_color = None
        self.figure.yaxis.minor_tick_line_color = None
        self.figure.yaxis.major_tick_line_color = None
        self.figure.xaxis.major_tick_line_color = None  # turn off y-axis major ticks
        self.figure.y_range.start = 0
        self.figure.xaxis.major_label_orientation = math.radians(45)
