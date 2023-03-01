import numpy as np
import pandas as pd
from bokeh.models import (
    BasicTicker,
    ColorBar,
    ColumnDataSource,
    HoverTool,
    LinearColorMapper,
)
from bokeh.palettes import Viridis256
from bokeh.plotting import figure
from bokeh.transform import transform

from TP4.modules.base.base_plot import BasePlot


class Heatmap(BasePlot):
    """
    Class implementation of the HeatMap plot primitive
    """

    def __init__(
            self, title, tools, palette=Viridis256, x_axis_label="", y_axis_label="", tooltips="", height=200, width=500, **params
    ):
        """
        Constructor of the HeatMap plot
        :param title: str
            title of the plot
        :param x_axis_label: str
            title of the xaxis
        :param y_axis_label: str
            title of the yaxis
        :param tools: list
            list of tools to use in the plot
        :param palette: list, default Viridis256
            list of colors to be used by the HeatMap
        :param tooltips: str, optional
            tooltips to be used by the HoverTool
        :param height: int
            plot height
        :param width: int
            plot width
        :param params: inherited args
        """
        super().__init__(**params)
        self.title = title
        self.tooltips = tooltips
        self.tools = tools
        self.palette = palette
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        if len(self.tooltips) > 0:
            self.hover = HoverTool(tooltips=self.tooltips)
            self.tools = [self.hover] + self.tools
        self.height = height
        self.width = width

        self.df = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=list("ABCD"))
        self.df = self.df.corr()

        self.df.index.name = "AllColumns1"
        self.df.columns.name = "AllColumns2"

        # Prepare data.frame in the right format
        self.df = self.df.stack().rename("value").reset_index()
        self.source = ColumnDataSource(data=self.df)

        self.make_figure()
        self.panel = self.get_panel()

    def update_heatmap(self, df):
        """
        At each refresh, update the heatmap with updated data
        :param df: padnas dataframe
            dataframe containing columns between which we want to compute correlation metric
        """
        self.df = df.corr()
        self.df.index.name = "AllColumns1"
        self.df.columns.name = "AllColumns2"
        # Prepare data.frame in the right format
        self.df = self.df.stack().rename("value").reset_index()
        self.figure.x_range.factors = list(self.df.AllColumns1.drop_duplicates())
        self.figure.y_range.factors = list(self.df.AllColumns2.drop_duplicates())
        self.source.data = self.df

        self.mapper.low = self.df.value.min()
        self.mapper.high = self.df.value.max()
        self.color_bar.color_mapper = self.mapper

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        self.mapper = LinearColorMapper(
            palette=self.palette, low=self.df.value.min(), high=self.df.value.max()
        )
        self.figure = figure(
            plot_width=self.width,
            plot_height=self.width,
            title=self.title,
            tools=self.tools,
            x_range=list(self.df.AllColumns1.drop_duplicates()),
            y_range=list(self.df.AllColumns2.drop_duplicates()),
            x_axis_location="below",
        )

        # Create rectangle for heatmap
        self.figure.rect(
            x="AllColumns1",
            y="AllColumns2",
            width=1,
            height=1,
            source=self.source,
            line_color=None,
            fill_color=transform("value", self.mapper),
        )

        # Add legend
        self.color_bar = ColorBar(
            color_mapper=self.mapper, location=(0, 0), ticker=BasicTicker(desired_num_ticks=10)
        )

        self.figure.add_layout(self.color_bar, "right")
        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label
