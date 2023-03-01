from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

from TP4.modules.base.base_plot import BasePlot


class LegendPlot(BasePlot):
    """
       Class implementation of the BasicLine plot primitive
       """

    def __init__(
            self,
            lines,
            colors,
            title="",
            height=150,
            width=80,
            **params
    ):

        super().__init__(**params)

        self.title = title
        self.lines = lines
        self.height = height
        self.width = width
        self.colors = colors
        self.legend_label = [x.replace("_", " ") for x in self.lines]
        self.legend_source = ColumnDataSource(
            data=dict(x=[1] * len(self.lines),
                      y=[2] * len(self.lines),
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
            height=self.height,
            width=self.width
        )

        if len(self.lines) > 1:
            self.figure.square(
                x="x",
                y="y",
                color=None,
                line_color=None,
                fill_color="legend_color",
                legend_field="legend_label",
                source=self.legend_source,
            )
        # Legend

        for rend in self.figure.renderers:
            rend.visible = False

        self.figure.toolbar_location = None
        self.figure.xaxis.axis_line_color = None
        self.figure.yaxis.axis_line_color = None
        self.figure.xaxis.major_tick_line_color = None  # turn off y-axis major ticks
        self.figure.outline_line_color = None

        self.figure.xaxis.visible = False
        self.figure.yaxis.visible = False
        self.figure.xgrid.grid_line_color = None
        self.figure.ygrid.grid_line_color = None
        self.figure.yaxis.minor_tick_line_color = None
        self.figure.yaxis.major_tick_line_color = None
        self.figure.outline_line_color = None
        self.figure.toolbar.logo = None

        self.figure.legend.background_fill_alpha = 0
        self.figure.legend.border_line_width = 0
