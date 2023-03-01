from bokeh.models import ColumnDataSource, HoverTool, LabelSet, Span
from bokeh.plotting import figure

from TP4.modules.scatterplots.base_scatterplot import BaseScatterPlot
from TP4.utils.formatters import NEW_Y_AXIS_FORMATTER


class BasicScatterPlot(BaseScatterPlot):
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
            data=dict(x=[], y=[], size=[], color=[], labels=[])
        )

        self.make_figure()
        self.panel = self.get_panel()

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        # Create plot
        self.figure = figure(tools=self.tools, plot_width=self.width, plot_height=self.height)
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
            text="labels",
            x_offset=0,
            y_offset=0,
            text_font_size="6pt",
            source=self.source,
        )
        self.figure.add_layout(labels)

        self.figure.toolbar.logo = None
        self.figure.y_range.start = 0
        self.figure.x_range.range_padding = 0
        self.figure.yaxis.minor_tick_line_color = None
        self.figure.xaxis.major_tick_line_color = None
        self.figure.yaxis.major_tick_line_color = None
        self.figure.xaxis.minor_tick_line_color = None
        self.figure.outline_line_color = None

        self.figure.yaxis.formatter = NEW_Y_AXIS_FORMATTER
