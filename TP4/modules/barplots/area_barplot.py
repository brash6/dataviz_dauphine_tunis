import math

from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LabelSet,
    LinearAxis,
    NumeralTickFormatter,
)
from bokeh.models.ranges import Range1d
from bokeh.plotting import figure

from TP4.modules.barplot import BarPlot
from TP4.utils.formatters import NEW_Y_AXIS_FORMATTER


class BarAreaPlot(BarPlot):
    """
    BarAreaPlot class implementation
    """

    def __init__(self, label=False, y2_axis_label="", **params):

        super().__init__(**params)
        self.label = label
        self.y2_axis_label = y2_axis_label

        # Initialise hover tool
        if len(self.tooltips) > 0:
            self.hover = HoverTool(tooltips=self.tooltips)
            self.hover.mode = "vline"
            self.tools = [self.hover] + self.tools

        self.source = ColumnDataSource(data=dict(x=[], y=[], y1=[], y2=[]))

        self.make_figure()
        self.panel = self.get_panel()

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        # Create plot
        self.figure = figure(
            x_range=self.x_axis_data,
            height=400,
            width=self.width,
            sizing_mode="scale_both",
            y_axis_label=self.title,
            tools=self.tools,
        )

        # Format X axis
        self.figure.x_range.range_padding = 0
        self.figure.xgrid.grid_line_color = None
        self.figure.xaxis.major_tick_line_color = None
        self.figure.xaxis.major_label_orientation = math.radians(45)

        # Format left Y axis
        self.figure.yaxis.formatter = NEW_Y_AXIS_FORMATTER
        self.figure.y_range.start = 0
        self.figure.yaxis.minor_tick_line_color = None
        self.figure.yaxis.major_tick_line_color = None
        self.figure.yaxis.axis_line_color = None
        self.figure.outline_line_color = None

        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label

        # Format right Y axis
        self.figure.extra_y_ranges = {
            "y2_name": Range1d(start=0, end=1.05)}
        y2_formatted = LinearAxis(y_range_name="y2_name",
                                  axis_label=self.y2_axis_label,
                                  minor_tick_line_color=None,
                                  major_tick_line_color=None,
                                  axis_line_color=None)
        y2_formatted.formatter = NumeralTickFormatter(format='0%')
        self.figure.add_layout(y2_formatted, 'right')

        # Add bar plot in the left Y-axis
        self.figure.vbar(
            x="x",
            top="y",
            source=self.source,
            width=0.7,
            line_color="White",
            fill_color=self.colors,
        )

        # Add area plot and scatter plot in the secondary Y-axis
        self.figure.varea(x="x", y1=0, y2="y2", color=self.colors, alpha=0.3, source=self.source, y_range_name="y2_name")
        self.figure.circle(x="x", y="y2", size=7, color=self.colors, source=self.source, y_range_name="y2_name")
        self.figure.line(x="x", y="y2", color=self.colors, source=self.source, y_range_name="y2_name")

        # Labels
        if self.label:
            labels = LabelSet(
                x="x",
                y="y",
                y1="y1",
                y2="y2",
                level="glyph",
                x_offset=-17.1,
                y_offset=-15,
                source=self.source,
                render_mode="canvas",
            )
            self.figure.add_layout(labels)

        self.figure.toolbar.logo = None
