import math

from bokeh.models import ColumnDataSource, HoverTool, LabelSet, Span
from bokeh.plotting import figure

from TP4.constants.constants import LR_SINGULAR_COLOR
from TP4.modules.barplots.base_barplot import BarPlot
from TP4.utils.formatters import NEW_Y_AXIS_FORMATTER


class IndexBarPlot(BarPlot):
    """
    Bar plot to visualise the evolution of values between 2 years index-wise
    """

    def __init__(self, label=False, **params):
        """
        Constructor of the Index Barplot
        :param params: inherited args
        """
        super().__init__(**params)
        self.label = label

        # Initialise hover tool
        if len(self.tooltips) > 0:
            self.hover = HoverTool(tooltips=self.tooltips)
            self.tools = [self.hover] + self.tools

        self.source = ColumnDataSource(
            data=dict(x=[], front=[], back=[], index_value=[], formatted_y2=[], color=[])
        )
        self.legend_source = ColumnDataSource(
            data=dict(x=[1, 2], y=[2, 1], legend_color=self.colors, legend_label=self.legend_label)
        )
        self.make_figure()
        self.panel = self.get_panel()

    def init_data(self):
        """
        At each refresh, update values to visualise
        """
        self.source.data["index_value"] = [
            100 * (front / back)
            for front, back in zip(self.source.data["front"], self.source.data["back"])
        ]
        self.source.data["formatted_y2"] = ["%0.1f" % x for x in self.source.data["index_value"]]
        self.source.data["color"] = self.init_color_list(threshold=100)

    def init_color_list(self, threshold):
        """
        At each resresh, update the colors of the bars to show depending on their values
        :param threshold: int
            value from which we change the color of the bar
        :return: list,
            colors which length is equal to the number of bars to show
        """
        color_list = []
        for i in self.source.data["index_value"]:
            if i > threshold + 5:
                color_list.append(self.colors[0])
            elif i < threshold - 5:
                color_list.append(self.colors[1])
            else:
                color_list.append(self.colors[2])
        return color_list

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        # Create plot
        self.figure = figure(x_range=self.x_axis_data, height=self.height, width=self.width,
                             sizing_mode="scale_both", tools=self.tools)

        hline = Span(location=100, dimension='width', line_color=LR_SINGULAR_COLOR, line_width=1, line_dash='dashed')
        self.figure.renderers.extend([hline])

        self.figure.vbar(x='x', top='index_value', fill_color='color', width=.7, source=self.source, line_color="White")

        # Labels
        if self.label:
            labels = LabelSet(
                x="x",
                y="index_value",
                text="formatted_y2",
                text_font_size="8pt",
                text_color="black",
                level="glyph",
                x_offset=-17,
                y_offset=2,
                source=self.source,
                render_mode="canvas",
            )
            self.figure.add_layout(labels)

        # Legend
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

        self.figure.y_range.start = 0
        self.figure.x_range.range_padding = 0
        self.figure.xaxis.major_label_orientation = math.radians(45)
        self.figure.xgrid.grid_line_color = None
        self.figure.yaxis.minor_tick_line_color = None
        self.figure.yaxis.major_tick_line_color = None
        self.figure.yaxis.axis_line_color = None
        self.figure.xaxis.minor_tick_line_color = None
        self.figure.xaxis.major_tick_line_color = None
        self.figure.outline_line_color = None
        self.figure.yaxis.formatter = NEW_Y_AXIS_FORMATTER
        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label
        self.figure.toolbar.logo = None
