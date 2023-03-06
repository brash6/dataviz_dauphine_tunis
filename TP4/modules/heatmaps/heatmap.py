import numpy as np
import pandas as pd
from bokeh.models import (
    BasicTicker,
    ColorBar,
    ColumnDataSource,
    FuncTickFormatter,
    HoverTool,
    LinearColorMapper,
)
from bokeh.palettes import Viridis256
from bokeh.plotting import figure

from TP4.modules.base.base_plot import BasePlot
from TP4.utils.formatters import SIMPLE_BARPLOT_FORMATTER


class Heatmap(BasePlot):
    """
    Class implementation of the HeatMap plot primitive
    """

    def __init__(
            self, title, tools, x, y, kpi, palette=Viridis256, x_axis_label="", y_axis_label="", tooltips="", height=200,
            width=500, **params
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
        :param kpi: str
            One kpi to plot among percentage_of_sales or quantity
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
        self.x = x
        self.y = y
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        if len(self.tooltips) > 0:
            self.hover = HoverTool(tooltips=self.tooltips)
            self.tools = [self.hover] + self.tools
        self.height = height
        self.width = width
        self.kpi = kpi

        # Init fake dataframe
        self.df = pd.DataFrame(np.random.randint(0, 10, size=(10, 3)),
                               columns=[self.y, self.x, self.kpi])
        self.df[self.y] = self.df[self.y].astype("str")
        self.df[self.x] = self.df[self.x].astype("str")

        # Prepare dataframe in the right format
        self.df_matrix = self.df.drop_duplicates([self.y, self.x]).pivot(self.y, self.x, self.kpi)
        self.df_matrix = self.df_matrix.fillna(0)
        self.source = ColumnDataSource(data=self.df)

        self.df_matrix.index.name = self.y
        self.df_matrix.columns.name = self.x

        self.make_figure()
        self.panel = self.get_panel()

    def update_heatmap(self, df):
        """
        At each refresh, update the heatmap with updated data
        :param df: pandas dataframe
            dataframe containing columns between which we want to compute correlation metric
        """
        self.df = df
        print(df)

        # Prepare dataframe in the right format
        self.df_matrix = df.pivot(self.y, self.x, self.kpi)
        self.df_matrix = self.df_matrix.fillna(0)
        print(self.df_matrix)

        self.df_matrix.index.name = self.y
        self.df_matrix.columns.name = self.x

        # Update ColumnDataSource & factors
        self.source.data = self.df
        self.figure.x_range.factors = list(self.df[self.x].drop_duplicates())
        self.figure.y_range.factors = list(self.df[self.y].drop_duplicates())

        self.mapper.low = self.df_matrix.min().min()
        self.mapper.high = self.df_matrix.max().max()
        self.color_bar.color_mapper = self.mapper

        # Style the x-axis
        self.figure.xaxis.formatter = FuncTickFormatter(
            code="""
                    if (tick.length > 30) return tick.substring(0, 30) + '...';
                    else return tick;
                """
        )

    def update_heatmap_correlation(self, df):
        corr = df.corr()
        self.df = corr.stack().reset_index().rename(columns={'level_0': self.x, 'level_1': self.y, 0: self.kpi})
        self.df_matrix = self.df.pivot(self.y, self.x, self.kpi)
        self.df_matrix = self.df_matrix.fillna(0)

        # Update ColumnDataSource & factors
        self.source.data = self.df
        self.figure.x_range.factors = list(self.df[self.x].drop_duplicates())
        self.figure.y_range.factors = list(self.df[self.y].drop_duplicates())

        self.mapper.low = self.df_matrix.min().min()
        self.mapper.high = self.df_matrix.max().max()
        self.color_bar.color_mapper = self.mapper

        # Style the x-axis
        self.figure.xaxis.formatter = FuncTickFormatter(
            code="""
                            if (tick.length > 30) return tick.substring(0, 30) + '...';
                            else return tick;
                        """
        )

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """

        self.mapper = LinearColorMapper(
            palette=self.palette, low=self.df_matrix.min().min(), high=self.df_matrix.max().max()
        )
        self.figure = figure(
            plot_width=self.width,
            plot_height=self.width,
            tools=self.tools,
            x_range=list(self.df_matrix.columns.astype('str')),
            y_range=list(self.df_matrix.index),
            x_axis_location="below",
        )

        # Create rectangle for heatmap
        self.figure.rect(
            x=self.x,
            y=self.y,
            width=1,
            height=1,
            source=self.source,
            line_color='white',
            line_width=1,
            fill_color={'field': self.kpi, 'transform': self.mapper},
        )

        # Add color bar
        self.color_bar = ColorBar(
            color_mapper=self.mapper,
            location=(0, 0), ticker=BasicTicker(desired_num_ticks=10)
        )

        self.figure.add_layout(self.color_bar, "right")

        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label

        self.figure.toolbar.logo = None
        self.figure.xaxis.axis_line_color = None
        self.figure.yaxis.axis_line_color = None
        self.figure.xgrid.grid_line_color = None
        self.figure.ygrid.grid_line_color = None
        self.figure.yaxis.minor_tick_line_color = None
        self.figure.yaxis.major_tick_line_color = None
        self.figure.xaxis.major_tick_line_color = None  # turn off y-axis major ticks
