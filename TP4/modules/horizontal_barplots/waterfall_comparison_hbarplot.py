from bokeh.models import ColumnDataSource, HoverTool, LabelSet, Span
from bokeh.plotting import figure

from TP4.modules.barplots.base_barplot import BarPlot


class WaterfallComparisonHBarPlot(BarPlot):
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
            data=dict(y=[], comparison_value=[], front=[], back=[], label=[], label_align=[], color=[])
        )

        self.make_figure()
        self.panel = self.get_panel()

    def init_data(self):
        """
        At each refresh, update values to visualise
        """
        self.source.data["comparison_value"] = [
            (front - back)
            for front, back in zip(self.source.data["front"], self.source.data["back"])
        ]
        self.source.data["label"] = [-1 if x > 0 else 1 for x in self.source.data["comparison_value"]]
        self.source.data["label_align"] = ['left' if x == 1 else 'right' for x in self.source.data["label"]]
        self.source.data["color"] = self.init_color_list(threshold=0)

    def init_color_list(self, threshold):
        """
        At each resresh, update the colors of the bars to show depending on their values
        :param threshold: int
            value from which we change the color of the bar
        :return: list,
            colors which length is equal to the number of bars to show
        """
        color_list = []
        for i in self.source.data["comparison_value"]:
            if i > threshold:
                color_list.append(self.colors[0])
            else:
                color_list.append(self.colors[1])
        return color_list

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        # Create plot
        self.figure = figure(y_range='init', x_range=(-10, 10), height=self.height, width=self.width,
                             sizing_mode="scale_both", tools=self.tools)
        self.figure.hbar(y='y', right='comparison_value', height=0.95, source=self.source,
                                   line_color="White", color="color")

        # Labels
        if self.label:
            labels = LabelSet(
                x="label",
                y="y",
                text="y",
                text_font_size="8pt",
                text_color="black",
                level="glyph",
                x_offset=0,
                y_offset=-5,
                text_align='label_align',
                source=self.source,
                render_mode="canvas",
            )
            self.figure.add_layout(labels)

        self.figure.y_range.range_padding = 0
        self.figure.yaxis.fixed_location = 0
        self.figure.yaxis.major_label_text_alpha = 0
        self.figure.outline_line_color = None
        self.figure.ygrid.grid_line_color = None
        self.figure.yaxis.minor_tick_line_color = None
        self.figure.yaxis.major_tick_line_color = None
        self.figure.xaxis.axis_line_color = None
        self.figure.xaxis.minor_tick_line_color = None
        self.figure.xaxis.major_tick_line_color = None
        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label
        self.figure.toolbar.logo = None
