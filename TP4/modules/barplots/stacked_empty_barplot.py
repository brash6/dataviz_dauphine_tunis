import pandas as pd
from bokeh.models import ColumnDataSource, HoverTool, LabelSet
from bokeh.plotting import figure

from TP4.modules.barplots.base_barplot import BarPlot
from TP4.utils.formatters import OVERLAPPING_BARPLOT_Y_AXIS_FORMATTER


class StackedHbarEmptyPlot(BarPlot):
    """
    Stacked Horizontal BarPlot class implementation
    """

    def __init__(self, stacked_option, display_legend=False, label=False, **params):
        """
        Constructor of StackedGroupedBarPlot class

        :param colors : str
            color of the bars
        :param params: inherited args
        """
        super().__init__(**params)
        self.label = label
        self.display_legend = display_legend
        self.stacked_option = stacked_option

        # Initialise hover tool
        if len(self.tooltips) > 0:
            self.hover = HoverTool(tooltips=self.tooltips)
            self.tools = [self.hover] + self.tools

        self.source = ColumnDataSource(data=dict(y=[], color=[], market_impact=[], share_impact=[], sales_dy=[]))
        self.make_figure()
        self.panel = self.get_panel()

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        # Create plot
        self.figure = figure(y_range=['XX', 'XY', 'XZ'],
                             width=self.width, height=self.height, tools=self.tools,
                             title='')

        self.figure.legend.background_fill_alpha = 0
        self.figure.legend.border_line_width = 0
        self.figure.legend.visible = False
        self.figure.toolbar.logo = None  # DO NOT CHANGE
        self.figure.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
        self.figure.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
        self.figure.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
        self.figure.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
        self.figure.yaxis.axis_line_color = None
        self.figure.xaxis.formatter = OVERLAPPING_BARPLOT_Y_AXIS_FORMATTER

        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label

        # Labels
        if self.label:
            market_labels = LabelSet(
                                    x='x_market',
                                    y="y",
                                    text="lbl_market",
                                    text_color="black",
                                    text_font_size="8pt",
                                    text_align='center',
                                    level="glyph",
                                    y_offset=-5,
                                    source=self.source,
                                    render_mode="canvas",
            )
            self.figure.add_layout(market_labels)

            share_labels = LabelSet(
                                    x='x_share',
                                    y="y",
                                    text="lbl_share",
                                    text_color="black",
                                    text_font_size="8pt",
                                    text_align='center',
                                    level="glyph",
                                    y_offset=-5,
                                    # x_offset=3,
                                    source=self.source,
                                    render_mode="canvas",
            )
            self.figure.add_layout(share_labels)
