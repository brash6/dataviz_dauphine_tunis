import math

from bokeh.models import ColumnDataSource, HoverTool, LinearAxis, Range1d
from bokeh.plotting import figure
from bokeh.transform import dodge

from TP4.modules.barplots.base_barplot import BarPlot
from TP4.utils.formatters import NEW_Y_AXIS_FORMATTER


class NestedBarPlot(BarPlot):
    """
    NestedBarPlot class implementation
    """

    def __init__(self, categories, double_y_axis=False, y2_axis_label="", **params):
        """
        Constructor of BasicBarPlot class

        :param colors : List [colors]
            colors of each category in categories, same length as categories
        :param categories : List [String]
            list of categories to compare
        :param params: inherited args
        """
        super().__init__(**params)
        self.categories = categories
        self.double_y_axis = double_y_axis
        self.y2_axis_label = y2_axis_label

        # Initialise hover tool
        if len(self.tooltips) > 0:
            self.hover = HoverTool(tooltips=self.tooltips)
            self.hover.mode = "vline"
            self.tools = [self.hover] + self.tools

        dict_source = {"x": []}
        for cat in self.categories:
            dict_source[cat] = []

        self.source = ColumnDataSource(data=dict_source)

        self.make_figure()
        self.panel = self.get_panel()

    def update_second_y_axis(self, min_y, max_y):
        """
        Update the additional y axis range values
        :param min_y: int
            min y range value
        :param max_y: int
            max y range value
        """
        self.figure.extra_y_ranges["y2_name"].start = min_y
        self.figure.extra_y_ranges["y2_name"].end = max_y

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

        # Format X axis
        self.figure.x_range.range_padding = 0.01
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
        if self.double_y_axis:
            self.figure.extra_y_ranges = {
                "y2_name": Range1d(start=0, end=10000)}
            y2_formatted = LinearAxis(y_range_name="y2_name",
                                      axis_label=self.y2_axis_label,
                                      minor_tick_line_color=None,
                                      major_tick_line_color=None,
                                      axis_line_color=None)

            y2_formatted.formatter = NEW_Y_AXIS_FORMATTER
            self.figure.add_layout(y2_formatted, 'right')

        # Add the bar plot
        step = 0.5/(len(self.categories)-1)
        bar_width = step - 0.05/(len(self.categories)-1)
        start = -0.25
        if len(self.categories) == 2:
            bar_width = 0.38
            start = -0.2
            step = 0.4
        for i, cat in enumerate(self.categories):
            if i == 1:
                if self.double_y_axis:
                    self.figure.vbar(
                        x=dodge("x", start + step * i, range=self.figure.x_range),
                        top=cat,
                        width=bar_width,
                        source=self.source,
                        y_range_name="y2_name",
                        color=self.colors[i],
                        legend_label=cat.replace("_", " "),
                    )
                else:
                    self.figure.vbar(
                        x=dodge("x", start + step * i, range=self.figure.x_range),
                        top=cat,
                        width=bar_width,
                        source=self.source,
                        color=self.colors[i],
                        legend_label=cat.replace("_", " "),
                    )
            else:
                self.figure.vbar(
                    x=dodge("x", start + step * i, range=self.figure.x_range),
                    top=cat,
                    width=bar_width,
                    source=self.source,
                    color=self.colors[i],
                    legend_label=cat.replace("_", " "),
                )
        self.figure.toolbar.logo = None
