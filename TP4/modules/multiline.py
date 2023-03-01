from bokeh.models import Band, ColumnDataSource, HoverTool
from bokeh.plotting import figure

from TP4.modules.base.base_plot import BasePlot
from TP4.utils.config_spinner import LoadingStyler


class MultiLine(BasePlot):
    """
    Class implementation of the MultiLine plot primitive
    """

    def __init__(
        self,
        cat_to_compare,
        title,
        legend_title,
        tools,
        x_axis_label="",
        y_axis_label="",
        tooltips="",
        height=600,
        width=1200,
        band_parameters=None,
        **params
    ):
        """
        Constructor of the MultiLine plot
        :param cat_to_compare: list
            categories to compare in the multiline plot
        :param x_axis_label: str
            x axis label
        :param y_axis_label: str
            y axis label
        :param title: str
            Plot title
        :param legend_title: str
            Legend title
        :param tools: list
            tools to be used by the plots
        :param tooltips: str, optional
            tooltips to be used by the HoverTool
        :param height: int
            plot height
        :param width: int
            plot width
        :param band_parameters: dict, optional
            To show a band inside the plot, has to have two keys : 'lower' and 'upper'
            Example : {"lower" : 15, "upper" : 18}
        :param params: inherited args
        """
        super().__init__(**params)

        self.tools = tools
        self.tooltips = tooltips
        # Initialise hover tool
        if len(self.tooltips) > 0:
            self.hover = HoverTool(tooltips=self.tooltips)
            self.tools = [self.hover] + self.tools

        self.cat_to_compare = cat_to_compare
        self.num_of_cat = len(self.cat_to_compare)
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.title = title
        self.legend_title = legend_title
        self.height = height
        self.width = width
        self.band_parameters = band_parameters

        self.create_dict_source()
        self.source = ColumnDataSource(self.dict_source)
        self.source_multiline = ColumnDataSource(data=dict(xs=[], ys=[], color=[], line_width=[]))

        self.styler = LoadingStyler(name="Styles")
        self.make_figure()
        self.panel = self.get_panel()

    def create_dict_source(self):
        """
        Initialize a dictionary to create the ColumDataSource with all needed inputs
        """
        dict_source = {"category": []}
        for cat in self.cat_to_compare:
            dict_source[cat + "_x"] = []
            dict_source[cat + "_y"] = []
        dict_source["color"] = []
        dict_source["line_width"] = []
        self.dict_source = dict_source

    def init_multiline_data(self):
        """
        At each refresh, update the multiline source data to update the lines to show
        """
        xs = []
        ys = []
        for cat in self.cat_to_compare:
            xs.append(self.source.data[cat + "_x"])
            ys.append(self.source.data[cat + "_y"])
        self.source_multiline.data["xs"] = xs
        self.source_multiline.data["ys"] = ys
        self.source_multiline.data["color"] = self.colors
        self.source_multiline.data["line_width"] = [2] * self.num_of_cat

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        self.figure = figure(
            tools=self.tools,
            title="",
            x_axis_type="datetime",
            plot_width=self.width,
            plot_height=self.height,
        )
        self.figure.legend.title = self.legend_title
        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label

        for i, cat in enumerate(self.cat_to_compare):
            self.figure.square(
                x=cat + "_x",
                y=cat + "_y",
                color=self.colors[i],
                legend_label=cat,
                source=self.source,
            )

        self.figure.multi_line(
            xs="xs", ys="ys", color="color", line_width="line_width", source=self.source_multiline
        )

        if self.band_parameters is not None:
            band = Band(
                base=self.cat_to_compare[0] + "_x",
                lower=self.band_parameters["lower"],
                upper=self.band_parameters["upper"],
                level="underlay",
                fill_alpha=0.1,
                line_width=1,
                line_color="black",
                fill_color="yellow",
                source=self.source,
            )
            self.figure.add_layout(band)

        self.figure.toolbar.logo = None
