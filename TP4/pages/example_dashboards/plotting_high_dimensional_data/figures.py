import math
import pandas as pd

from bokeh.models import ColumnDataSource, HoverTool, LabelSet, Whisker
from bokeh.plotting import figure
from bokeh.sampledata.autompg2 import autompg2
from bokeh.transform import factor_cmap

from TP4.constants.constants import LR_SINGULAR_COLOR
from TP4.modules.barplots.base_barplot import BarPlot
from TP4.utils.formatters import NEW_Y_AXIS_FORMATTER, format_label


class BoxPlot(BarPlot):
    """
    BasicBarPlot class implementation
    """

    def __init__(self, df, **params):
        super().__init__(**params)

        self.df = df

        self.kinds = list(self.df["kind"].astype(str).unique())

        # compute quantiles
        qs = self.df.groupby("kind").hwy.quantile([0.25, 0.5, 0.75])
        qs = qs.unstack().reset_index()
        qs.columns = ["kind", "q1", "q2", "q3"]
        self.df = pd.merge(self.df, qs, on="kind", how="left")

        # compute IQR outlier bounds
        iqr = self.df.q3 - self.df.q1
        self.df["upper"] = self.df.q3 + 1.5 * iqr
        self.df["lower"] = self.df.q1 - 1.5 * iqr

        print(self.df)

        self.source = ColumnDataSource(self.df)

        self.make_figure()
        self.panel = self.get_panel()

    def update_boxplots(self, data):
        self.df = data
        self.kinds = list(self.df["kind"].astype(str).unique())

        qs = self.df.groupby("kind").hwy.quantile([0.25, 0.5, 0.75])
        qs = qs.unstack().reset_index()
        qs.columns = ["kind", "q1", "q2", "q3"]
        self.df = pd.merge(self.df, qs, on="kind", how="left")

        print(self.df)

        # compute IQR outlier bounds
        iqr = self.df.q3 - self.df.q1
        self.df["upper"] = self.df.q3 + 1.5 * iqr
        self.df["lower"] = self.df.q1 - 1.5 * iqr

        print(self.df)

        self.source = ColumnDataSource(self.df)
        self.outliers = ColumnDataSource(self.df[~self.df.hwy.between(self.df.lower, self.df.upper)])

    def proprocess_for_boxplot(self, data):
        df = pd.DataFrame()
        for col in list(data.columns.values):
            df_col = data[col]
            df_col["kind"] = col
            df = df.append(df_col)
        print(df)
        return df

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        # Create plot
        self.figure = figure(
            x_range=self.kinds,
            toolbar_location=None,
            tools="",
            x_axis_label=self.x_axis_label,
            y_axis_label=self.y_axis_label,
        )

        # outlier range
        whisker = Whisker(base="kind", upper="upper", lower="lower", source=self.source)
        whisker.upper_head.size = whisker.lower_head.size = 20
        self.figure.add_layout(whisker)

        # quantile boxes
        self.figure.vbar("kind", 0.7, "q2", "q3", source=self.source, color=LR_SINGULAR_COLOR, line_color="black")
        self.figure.vbar("kind", 0.7, "q1", "q2", source=self.source, color=LR_SINGULAR_COLOR, line_color="black")

        # outliers
        self.outliers = ColumnDataSource(self.df[~self.df.hwy.between(self.df.lower, self.df.upper)])
        self.figure.scatter("kind", "hwy", source=self.outliers, size=6, color="black", alpha=0.3)

        self.figure.y_range.start = 0
        self.figure.x_range.range_padding = 0
        self.figure.xaxis.major_label_orientation = math.radians(45)
        self.figure.xgrid.grid_line_color = None
        self.figure.yaxis.minor_tick_line_color = None
        self.figure.xaxis.major_tick_line_color = None
        self.figure.yaxis.major_tick_line_color = None
        self.figure.yaxis.axis_line_color = None
        self.figure.outline_line_color = None

        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label

        self.figure.toolbar.logo = None
