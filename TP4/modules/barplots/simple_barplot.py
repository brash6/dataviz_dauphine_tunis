import math

from bokeh.models import ColumnDataSource, HoverTool, LabelSet
from bokeh.plotting import figure

from TP4.modules.barplots.base_barplot import BarPlot
from TP4.utils.formatters import NEW_Y_AXIS_FORMATTER, format_label


class SimpleBarPlot(BarPlot):
    """
    BasicBarPlot class implementation
    """

    def __init__(self, label=False, **params):
        """
        Constructor of BasicBarPlot class

        :param colors : str
            color of the bars
        :param params: inherited args
        """
        super().__init__(**params)
        self.label = label

        # Initialise hover tool
        if len(self.tooltips) > 0:
            self.hover = HoverTool(tooltips=self.tooltips)
            self.hover.mode = "vline"
            self.tools = [self.hover] + self.tools

        self.source = ColumnDataSource(data=dict(x=[], y=[], formatted_y=[]))

        self.make_figure()
        self.panel = self.get_panel()

    def init_formatted_y(self):
        """
        Format y axis of the BasicBarPlot using format_label() function
        """
        self.source.data["formatted_y"] = [
            format_label(float(x)) for x in self.source.data["y"]
        ]

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        # Create plot
        self.figure = figure(
            x_range=self.x_axis_data,
            height=self.height,
            width=self.width,
            tooltips=self.tooltips,
            sizing_mode="scale_both",
            tools=self.tools,
        )
        self.figure.vbar(
            x="x",
            top="y",
            source=self.source,
            width=0.7,
            line_color="White",
            fill_color=self.colors,
        )
        self.figure.y_range.start = 0
        self.figure.x_range.range_padding = 0
        self.figure.xaxis.major_label_orientation = math.radians(45)
        self.figure.xgrid.grid_line_color = None
        self.figure.yaxis.minor_tick_line_color = None
        self.figure.xaxis.major_tick_line_color = None
        self.figure.yaxis.major_tick_line_color = None
        self.figure.yaxis.axis_line_color = None
        self.figure.outline_line_color = None

        self.figure.yaxis.formatter = NEW_Y_AXIS_FORMATTER

        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label

        # Labels
        if self.label:
            labels = LabelSet(
                x="x",
                y="y",
                text="formatted_y",
                text_color="black",
                text_font_size="7pt",
                level="glyph",
                x_offset=-17.1,
                y_offset=+1,
                source=self.source,
                render_mode="canvas",
            )
            self.figure.add_layout(labels)

        self.figure.toolbar.logo = None
