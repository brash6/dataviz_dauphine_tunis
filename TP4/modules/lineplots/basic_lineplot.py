import math

from bokeh.models import Circle, ColumnDataSource, FuncTickFormatter, HoverTool, Line
from bokeh.plotting import figure

from TP4.modules.lineplots.base_lineplot import LinePlot
from TP4.utils.formatters import NEW_Y_AXIS_FORMATTER


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


class BasicLinePlot(LinePlot):
    """
    Class implementation of the BasicLine plot primitive
    """

    def __init__(
            self,
            lines,
            line_width=2,
            size=4,
            **params
    ):

        super().__init__(**params)

        # Initialise hover tool
        if len(self.tooltips) > 0:
            self.hover = HoverTool(tooltips=self.tooltips)
            self.tools = [self.hover] + self.tools

        self.line_width = line_width
        self.size = size

        self.lines = lines

        dict_source = {"x": []}
        for elem in self.lines:
            dict_source[elem] = []

        self.source = ColumnDataSource(data=dict_source)

        self.legend_label = [x.replace("_", " ") for x in self.lines]

        self.legend_source = ColumnDataSource(
            data=dict(x=[1]*len(self.lines),
                      y=[2]*len(self.lines),
                      legend_color=self.colors[:len(self.lines)],
                      legend_label=self.legend_label)
        )

        self.make_figure()
        self.panel = self.get_panel()

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        self.figure = figure(
            x_range=self.x_axis_data,
            tools=self.tools,
            height=self.height,
            width=self.width
        )
        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label

        for i, elem in enumerate(self.lines):
            self.line = Line(x="x", y=elem, line_color=self.colors[i], line_width=self.line_width)

            self.circle = Circle(x="x", y=elem, line_color=self.colors[i], fill_color="white",
                                 line_width=self.line_width,
                                 size=self.size,
                                 )

            self.figure.add_glyph(self.source, self.line)
            self.figure.add_glyph(self.source, self.circle)

        # Legend
        if len(self.lines) > 1:
            self.figure.circle(
                x="x",
                y="y",
                radius=0,
                color=None,
                line_color=None,
                fill_color="legend_color",
                legend_field="legend_label",
                source=self.legend_source,
            )

        self.figure.toolbar.logo = None
        self.figure.xaxis.axis_line_color = None
        self.figure.yaxis.axis_line_color = None
        self.figure.xgrid.grid_line_color = None
        self.figure.yaxis.minor_tick_line_color = None
        self.figure.yaxis.major_tick_line_color = None
        self.figure.xaxis.major_tick_line_color = None  # turn off y-axis major ticks
        self.figure.outline_line_color = None
        self.figure.y_range.start = 0
        self.figure.xaxis.major_label_orientation = math.radians(45)
        self.figure.yaxis.formatter = NEW_Y_AXIS_FORMATTER
