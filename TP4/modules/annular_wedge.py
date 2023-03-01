import math

from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.transform import cumsum

from TP4.modules.base.base_plot import BasePlot


class AnnularWedge(BasePlot):
    """
    Class implementation of the AnnularWedge Plot primitive
    """

    def __init__(
        self,
        title,
        format="2pi",
        legend_title="",
        tooltips="",
        colors="",
        tools="",
        height=600,
        width=1200,
        **params
    ):
        """
        Constructor of the AnnularWedge plot primitive
        :param title: str
            plot title
        :param format: str, default "2pi"
            format of the annular wedge, default 2pi for a complete annular wedge, use pi for a half annularwedge
        :param legend_title: str
            legend title
        :param tooltips: str
            tooltips used by the HoverTool
        :param colors: list
            colors used by the plot
        :param tools: list
            Bokeh tools to be used by the plot
        :param height: int
            height of the plot
        :param width: int
            width of the plot
        :param params: inherited args
        """
        super().__init__(**params)

        self.tools = tools
        if len(tooltips) > 0:
            self.hover = HoverTool(tooltips=tooltips)
            self.tools = [self.hover] + self.tools
            # https://github.com/bokeh/bokeh/issues/9492
        self.title = title
        self.format = format
        self.colors = colors
        self.legend_title = legend_title
        self.tooltips = tooltips
        self.height = height
        self.width = width
        self.source = ColumnDataSource(
            data=dict(categories=[], values=[], pourcentage=[], angle=[], color=[])
        )

        self.make_figure()
        self.panel = self.get_panel()

    def init_angle_and_pourcentage(self):
        """
        At each refresh, update the angle and the pourcentage values for rendering
        """
        values = self.source.data["values"]
        if self.format == "2pi":
            self.source.data["angle"] = [2 * math.pi * (x / sum(values)) for x in values]
        elif self.format == "pi":
            self.source.data["angle"] = [math.pi * (x / sum(values)) for x in values]
        self.source.data["pourcentage"] = [100 * x / sum(values) for x in values]

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        self.figure = figure(
            x_range=(-1, 1),
            y_range=(-1, 1),
            plot_height=self.height,
            plot_width=self.width,
            title=self.title,
            toolbar_location=None,
            tools=self.tools,
            match_aspect=True,
        )
        self.figure.annular_wedge(
            x=0,
            y=0,
            inner_radius=0.15,
            outer_radius=0.25,
            direction="anticlock",
            start_angle=cumsum("angle", include_zero=True),
            end_angle=cumsum("angle"),
            line_color="white",
            fill_color="color",
            legend="categories",
            source=self.source,
        )

        self.figure.xaxis.visible = False
        self.figure.yaxis.visible = False
        self.figure.xgrid.visible = False
        self.figure.ygrid.visible = False
        self.figure.outline_line_color = None
        self.figure.legend[0].label_text_font_size = "7pt"
