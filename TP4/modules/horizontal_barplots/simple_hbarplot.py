from bokeh.models import ColumnDataSource, FuncTickFormatter, HoverTool, LabelSet
from bokeh.plotting import figure
from numerize import numerize

from TP4.modules.barplots.base_barplot import BarPlot
from TP4.utils.formatters import override_numerize


class SimpleHBarPlot(BarPlot):
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
            self.hover.mode = "hline"
            self.tools = [self.hover] + self.tools

        self.source = ColumnDataSource(data=dict(y=[], x=[], formatted_x=[]))

        self.make_figure()
        self.panel = self.get_panel()

    def init_formatted_x(self, x, value_format="num"):
        """
        Format x axis using numerize() function
        """
        if value_format == 'percentage':
            formatted_x = ['{:.1%}'.format(element) for element in x]
        elif value_format == 'num':
            formatted_x = [override_numerize(element) for element in x]
        elif value_format == 'monetary':
            formatted_x = ["€{:,.2f}".format(element) for element in x]
        else:
            formatted_x = x

        return formatted_x

    def update(self, max_x):
        """
        At each refresh, update x axis range values
        :param min_x: float
            min value
        :param max_x: float
            max value
        """
        self.figure.x_range.start = 0
        self.figure.x_range.end = max_x * 1.15

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        # Create plot
        self.figure = figure(
            y_range=self.x_axis_data,
            x_range=(0, 20),
            height=self.height,
            width=self.width,
            sizing_mode="scale_both",
            tools=self.tools,
        )
        self.figure.hbar(
            y="y",
            right="x",
            source=self.source,
            height=0.95,
            line_color="White",
            fill_color=self.colors,
        )

        # Labels
        if self.label:
            labels = LabelSet(
                x="x",
                y="y",
                text="formatted_x",
                x_units='data',
                y_units='data',
                x_offset=5,
                text_baseline="center",
                text_color="black",
                text_font_size="8pt",
                level="glyph",
                source=self.source,
                render_mode="css",
            )
            self.figure.add_layout(labels)

        self.figure.toolbar.logo = None
        # Style the axis
        self.figure.outline_line_color = None
        self.figure.y_range.range_padding = 0
        self.figure.xaxis.axis_line_color = None
        self.figure.ygrid.grid_line_color = None
        self.figure.yaxis.minor_tick_line_color = None
        self.figure.xaxis.minor_tick_line_color = None
        self.figure.yaxis.major_tick_line_color = None
        self.figure.xaxis.major_tick_line_color = None
        self.figure.yaxis.formatter = FuncTickFormatter(
            code="""
                            if (tick.length > 30) return tick.substring(0, 30) + '...';
                            else return tick;
                        """
        )
        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label
