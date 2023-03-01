import math

from bokeh.models import (
    ColumnDataSource,
    FuncTickFormatter,
    HoverTool,
    LabelSet,
    LinearAxis,
    NumeralTickFormatter,
    Range1d,
    Rect,
)
from bokeh.plotting import figure
from bokeh.transform import dodge

from TP4.modules.base.base_plot import BasePlot
from TP4.utils.formatters import (
    MSMT_SIMPLE_BARPLOT_FORMATTER,
    NEW_Y_AXIS_FORMATTER,
    OVERLAPPING_BARPLOT_Y_AXIS_FORMATTER,
    SIMPLE_BARPLOT_FORMATTER,
    STACKED_BARPLOT_FORMATTER,
    currency_mapper,
    format_label,
    format_label_euro,
)


class BarPlot(BasePlot):
    """
    Class implementation for basic barplot
    """

    def __init__(
            self,
            x_axis_data,
            title,
            x_axis_label="",
            y_axis_label="",
            legend_title="",
            legend_label="",
            tooltips="",
            colors="",
            tools="",
            height=600,
            width=1200,
            **params
    ):
        """
        Constructor of a basic barplot
        :param x_axis_data: list
            x axis data used for plot initialization
        :param title: str
            plot title
        :param x_axis_label: str
            x axis label
        :param y_axis_label: str
            y axis label
        :param legend_title: str, optional
            legend title
        :param legend_label: list, optional
            legend labels
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
        self.x_axis_data = x_axis_data
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.tools = tools
        self.title = title
        self.colors = colors
        self.legend_title = legend_title
        self.legend_label = legend_label
        self.tooltips = tooltips
        self.height = height
        self.width = width
        self.source = ColumnDataSource(data=dict(x=[], y=[]))


class BasicBarPlot(BarPlot):
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
            self.hover.mode = "vline"
            self.tools = [self.hover] + self.tools

        self.source = ColumnDataSource(data=dict(x=[], y=[], formatted_y=[]))

        self.make_figure()
        self.panel = self.get_panel()

    def init_formatted_y(self):
        """
        Format y axis of the BasicBarPlot using format_label() function
        """
        self.source.data["formatted_y"] = [
            format_label(float(x)) for x in self.source.data["y"]
        ]

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        # Create plot
        self.figure = figure(
            x_range=self.x_axis_data,
            height=self.height,
            width=self.width,
            tooltips=self.tooltips,
            sizing_mode="scale_both",
            tools=self.tools,
        )
        self.figure.vbar(
            x="x",
            top="y",
            source=self.source,
            width=0.7,
            line_color="White",
            fill_color=self.colors,
        )
        self.figure.y_range.start = 0
        self.figure.x_range.range_padding = 0
        self.figure.xaxis.major_label_orientation = math.radians(45)
        self.figure.xgrid.grid_line_color = None
        self.figure.yaxis.minor_tick_line_color = None
        self.figure.xaxis.major_tick_line_color = None
        self.figure.yaxis.major_tick_line_color = None
        self.figure.yaxis.axis_line_color = None

        self.figure.yaxis.formatter = NEW_Y_AXIS_FORMATTER

        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label

        # Labels
        if self.label:
            labels = LabelSet(
                x="x",
                y="y",
                text="formatted_y",
                text_color="black",
                text_font_size="7pt",
                level="glyph",
                x_offset=-17.1,
                y_offset=+1,
                source=self.source,
                render_mode="canvas",
            )
            self.figure.add_layout(labels)

        self.figure.toolbar.logo = None


class NestedBarPlot(BarPlot):
    """
    NestedBarPlot class implementation
    """

    def __init__(self, categories, double_y_axis=False, y2_axis_label="", **params):
        """
        Constructor of BasicBarPlot class

        :param colors : List [colors]
            colors of each category in categories, same length as categories
        :param categories : List [String]
            list of categories to compare
        :param params: inherited args
        """
        super().__init__(**params)
        self.categories = categories
        self.double_y_axis = double_y_axis
        self.y2_axis_label = y2_axis_label

        # Initialise hover tool
        if len(self.tooltips) > 0:
            self.hover = HoverTool(tooltips=self.tooltips)
            self.hover.mode = "vline"
            self.tools = [self.hover] + self.tools

        dict_source = {"x": []}
        for cat in self.categories:
            dict_source[cat] = []

        self.source = ColumnDataSource(data=dict_source)

        self.make_figure()
        self.panel = self.get_panel()

    def update_second_y_axis(self, min_y, max_y):
        """
        Update the additional y axis range values
        :param min_y: int
            min y range value
        :param max_y: int
            max y range value
        """
        self.figure.extra_y_ranges["y2_name"].start = min_y
        self.figure.extra_y_ranges["y2_name"].end = max_y

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        # Create plot
        self.figure = figure(
            x_range=self.x_axis_data,
            height=self.height,
            width=self.width,
            tooltips=self.tooltips,
            sizing_mode="scale_both",
            tools=self.tools,
        )

        # Format X axis
        self.figure.x_range.range_padding = 0.01
        self.figure.xgrid.grid_line_color = None
        self.figure.xaxis.major_tick_line_color = None
        self.figure.xaxis.major_label_orientation = math.radians(45)

        # Format left Y axis
        self.figure.yaxis.formatter = NEW_Y_AXIS_FORMATTER
        self.figure.y_range.start = 0
        self.figure.yaxis.minor_tick_line_color = None
        self.figure.yaxis.major_tick_line_color = None
        self.figure.yaxis.axis_line_color = None

        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label

        # Format right Y axis
        if self.double_y_axis:
            self.figure.extra_y_ranges = {
                "y2_name": Range1d(start=0, end=10000)}
            y2_formatted = LinearAxis(y_range_name="y2_name",
                                      axis_label=self.y2_axis_label,
                                      minor_tick_line_color=None,
                                      major_tick_line_color=None,
                                      axis_line_color=None)

            y2_formatted.formatter = NEW_Y_AXIS_FORMATTER
            self.figure.add_layout(y2_formatted, 'right')

        # Add the bar plot
        for i, cat in enumerate(self.categories):
            if i == 1:
                if self.double_y_axis:
                    self.figure.vbar(
                        x=dodge("x", -0.25 + i / 2, range=self.figure.x_range),
                        top=cat,
                        width=0.38,
                        source=self.source,
                        y_range_name="y2_name",
                        color=self.colors[i],
                        legend_label=cat.replace("_", " "),
                    )
                else:
                    self.figure.vbar(
                        x=dodge("x", -0.25 + i / 2, range=self.figure.x_range),
                        top=cat,
                        width=0.38,
                        source=self.source,
                        color=self.colors[i],
                        legend_label=cat.replace("_", " "),
                    )
            else:
                self.figure.vbar(
                    x=dodge("x", -0.13 + i / 2, range=self.figure.x_range),
                    top=cat,
                    width=0.38,
                    source=self.source,
                    color=self.colors[i],
                    legend_label=cat.replace("_", " "),
                )
        self.figure.toolbar.logo = None


class OverlappingBarplot(BarPlot):
    """
    OverlappingBarplot class
    """

    def __init__(self, label=False, **params):
        """
        Constructor of OverlappingBarplot class
        :param params: inherited args
        """
        super().__init__(**params)
        self.label = label

        # Initialise hover tool
        if len(self.tooltips) > 0:
            self.hover = HoverTool(tooltips=self.tooltips)
            self.hover.mode = "vline"
            self.tools = [self.hover] + self.tools

        self.source = ColumnDataSource(
            data=dict(x=[], front=[], back=[], rect_center=[], rect_width=[], formatted_y=[])
        )
        self.legend_source = ColumnDataSource(
            data=dict(x=[1, 2], y=[2, 1], legend_color=self.colors, legend_label=self.legend_label)
        )
        self.make_figure()
        self.panel = self.get_panel()

    def init_rect_center_and_width(self, front, back):
        """
        At each refresh, update the rect centers and the rect widths of the rect glyphs (beside bars)
        :param back: list
            values to visualise on the rect glyphs
        :param front: list
            values to visualise on the front bars
        """
        rect_width = []
        for i in range(len(back)):
            if back[i] < front[i]:
                rect_width.append(0.9)
            else:
                rect_width.append(0.5)
        rect_center = [x / 2 for x in back]
        return rect_center, rect_width

    def init_formatted_y(self):
        """
        Format y axis of the OverlappingBarplot using format_label() function
        """
        self.source.data["formatted_y"] = [
            format_label(x) + "€" for x in self.source.data["front"]
        ]

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        # Create plot
        self.figure = figure(x_range=self.x_axis_data, height=self.height, width=self.width,
                             tooltips=self.tooltips, sizing_mode="scale_both",
                             tools=self.tools)
        self.glyph = Rect(x="x", y="rect_center", width='rect_width', height="back", fill_alpha=0.4,
                          fill_color=self.colors[1], line_color=None)
        self.figure.add_glyph(self.source, self.glyph)
        self.figure.vbar(
            x="x",
            top="front",
            source=self.source,
            width=0.7,
            line_color="White",
            fill_color=self.colors[0],
        )

        # Labels
        if self.label:
            labels = LabelSet(
                x="x",
                y="front",
                text="formatted_y",
                text_color="white",
                text_font_size="7pt",
                level="glyph",
                x_offset=-17.1,
                y_offset=-15,
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
        self.figure.yaxis.formatter = NEW_Y_AXIS_FORMATTER
        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label
        self.figure.toolbar.logo = None


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
            if i > threshold + 10:
                color_list.append(self.colors[0])
            elif i < threshold - 10:
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
        self.figure.vbar(x='x', top='index_value', fill_color='color', width=.7, source=self.source, line_color="White")

        # Labels
        if self.label:
            labels = LabelSet(
                x="x",
                y="index_value",
                text="formatted_y2",
                text_font_size="8pt",
                text_color="white",
                level="glyph",
                x_offset=-13.1,
                y_offset=-15,
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
        self.figure.yaxis.formatter = NEW_Y_AXIS_FORMATTER
        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label
        self.figure.toolbar.logo = None


class DYABarPlot(BarPlot):
    """
    Class implementation of DYABarplot to visualize the evolution of values between 2 periods value-wise
    """

    def __init__(self, barplot, **params):
        """
        Constructor of the DYABarplot
        :param barplot: OverlappingBarplot
            related barplot to use to make the plot
        :param params: inherited args
        """
        super().__init__(**params)

        # Initialise hover tool
        if len(self.tooltips) > 0:
            self.hover = HoverTool(tooltips=self.tooltips)
            self.tools = [self.hover] + self.tools

        self.barplot = barplot
        self.source = self.barplot.source
        self.legend_source = ColumnDataSource(
            data=dict(x=[1, 2], y=[2, 1], legend_color=self.colors, legend_label=self.legend_label)
        )
        self.make_figure()
        self.panel = self.get_panel()

    def init_data(self):
        """
        At each refresh, update values to visualise
        """
        self.source = self.barplot.source
        self.source.data["dya_value"] = [
            (i2021 - i2020)
            for i2021, i2020 in zip(self.source.data["current"], self.source.data["yag"])
        ]
        self.source.data["formatted_dya"] = [
            format_label_euro(x) for x in self.source.data["dya_value"]
        ]
        self.source.data["color"] = self.init_color_list(threshold=0)

    def init_color_list(self, threshold):
        """
        At each refresh, update colors of the bars to show
        :param threshold: int
            value from which we change the color of the bar
        :return: list
            colors which length is equal to the number of bars to show
        """
        color_list = []
        for i in self.source.data["dya_value"]:
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
        self.figure = figure(x_range=self.barplot.x_axis_data, height=self.height, width=self.width,
                             sizing_mode="scale_both", y_axis_label=self.title, tools=self.tools, min_border_left=150)
        self.figure.vbar(x='x', top='dya_value', fill_color='color', width=.7, source=self.source)

        self.figure.title.text = ""
        self.figure.x_range.range_padding = 0
        self.figure.xaxis.major_label_orientation = math.radians(45)
        self.figure.xaxis.major_label_text_font_style = "bold"
        self.figure.xgrid.grid_line_color = None
        self.figure.yaxis.minor_tick_line_color = None
        self.figure.yaxis.formatter = OVERLAPPING_BARPLOT_Y_AXIS_FORMATTER
        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label

        # Labels
        labels = LabelSet(
            x="x",
            y="dya_value",
            text="formatted_dya",
            text_font_size="8pt",
            text_color="black",
            level="glyph",
            x_offset=-13.1,
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

        self.figure.toolbar.logo = None


class StackedBarPlot(BarPlot):
    """
    Class implementation of the StackedBarplot
    """

    # https://stackoverflow.com/questions/59372635/vbar-stack-bokeh-update-from-dropdown
    def __init__(self, stacked_categories, label=False, **params):
        """
        Constructor of the StackedBarPlot
        :param stacked_categories: list
            Categories to stack in the bar plot
        :param params: inherited args
        """
        super().__init__(**params)

        # Initialise hover tool
        if len(self.tooltips) > 0:
            self.hover = HoverTool(tooltips=self.tooltips)
            self.tools = [self.hover] + self.tools

        self.stacked_categories = stacked_categories
        self.label = label
        self.data_dict = {"x": self.x_axis_data}
        for channel in stacked_categories:
            self.data_dict[channel] = []
            self.data_dict[channel + '_label'] = []
            self.data_dict['y_' + channel + '_offset'] = []
        self.source = ColumnDataSource(data=self.data_dict)

        self.make_figure()
        self.panel = self.get_panel()

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        self.figure = figure(x_range=self.x_axis_data, height=self.height, width=int(self.width * 0.7),
                             sizing_mode="scale_width",
                             title="", tools=self.tools)
        self.figure.vbar_stack(stackers=self.stacked_categories, x='x', width=0.9, color=self.colors,
                               source=self.source,
                               legend_label=[str(x).capitalize().replace('_', ' ') for x in self.stacked_categories])
        self.figure.yaxis.formatter = STACKED_BARPLOT_FORMATTER
        self.figure.legend.title = self.legend_title
        self.figure.xaxis.major_label_orientation = math.radians(45)
        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label

        self.figure.xaxis.formatter = FuncTickFormatter(
            code="""
                            if (tick.length > 30) return tick.substring(0, 30) + '...';
                            else return tick;
                        """
        )

        self.figure.y_range.start = 0
        self.figure.xgrid.grid_line_color = None
        self.figure.xaxis.major_tick_line_color = None  # turn off y-axis major ticks
        self.figure.yaxis.minor_tick_line_color = None
        self.figure.yaxis.major_tick_line_color = None
        self.figure.xaxis.axis_line_color = None
        self.figure.yaxis.axis_line_color = None
        self.figure.toolbar.logo = None

        # Labels
        label_list = [x + '_label' for x in self.stacked_categories]
        y_label_offset = ['y_' + x + '_offset' for x in self.stacked_categories]
        if self.label:
            for label_text, y_label_offset in zip(label_list, y_label_offset):
                labels = LabelSet(
                    x="x",
                    y=y_label_offset,
                    text=label_text,
                    text_color="black",
                    text_font_size="10pt",
                    level="glyph",
                    x_offset=-15,
                    y_offset=-10,
                    source=self.source,
                    render_mode="canvas"
                )
                self.figure.add_layout(labels)

class HorizontalBarPlot(BarPlot):
    """
    Class implementation of the HorizontalBarPlot
    """

    # https://stackoverflow.com/questions/59372635/vbar-stack-bokeh-update-from-dropdown
    def __init__(self, stacked_categories, bar_height=0.2, bar_shift_start=-0.3, bar_shift=0.6, **params):
        """
        Constructor of the HorizontalBarPlot
        :param stacked_categories: list
            Categories to stack
        :param params: inherited args
        """
        super().__init__(**params)

        # Initialise hover tool
        if len(self.tooltips) > 0:
            self.hover = HoverTool(tooltips=self.tooltips)
            self.tools = [self.hover] + self.tools

        self.stacked_categories = stacked_categories
        self.bar_height = bar_height
        self.bar_shift_start = bar_shift_start
        self.bar_shift = bar_shift

        self.data_dict = {"x": self.x_axis_data}
        for channel in stacked_categories:
            self.data_dict[channel] = []

        self.source = ColumnDataSource(data=self.data_dict)

        self.make_figure()
        self.panel = self.get_panel()

    def update(self, min_x, max_x):
        """
        At each refresh, update x axis range values
        :param min_x: float
            min value
        :param max_x: float
            max value
        """
        self.figure.x_range = Range1d(start=min_x, end=max_x)

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        self.figure = figure(
            y_range=self.x_axis_data,
            x_range=(-150000, 250000),
            height=self.height,
            width=self.width,
            sizing_mode="scale_both",
            title="",
            tools=self.tools,
        )
        i = 0
        for j, category in enumerate(self.stacked_categories):
            self.figure.hbar(
                y=dodge("x", self.bar_shift_start + i, range=self.figure.y_range),
                right=category,
                height=self.bar_height,
                source=self.source,
                color=self.colors[j],
                legend_label=category,
            )
            i += self.bar_shift

        self.figure.legend.title = self.legend_title
        self.figure.legend[0].items.reverse()

        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label

        self.figure.toolbar.logo = None


class NonStackedHorizontalBarPlot(BarPlot):
    """
    Class implementation of the HorizontalBarPlot
    """

    # https://stackoverflow.com/questions/59372635/vbar-stack-bokeh-update-from-dropdown
    def __init__(self, bar_height=1, **params):
        """
        Constructor of the NonStackedHorizontalBarPlot

        :param params: inherited args
        """
        super().__init__(**params)
        self.bar_height = bar_height

        # Initialise hover tool
        if len(self.tooltips) > 0:
            self.hover = HoverTool(tooltips=self.tooltips)
            self.tools = [self.hover] + self.tools

        self.data_dict = {"categories": self.x_axis_data, "values": []}

        self.source = ColumnDataSource(data=self.data_dict)

        self.make_figure()
        self.panel = self.get_panel()

    def update(self, min_x, max_x):
        """
        At each refresh, update x axis range values
        :param min_x: float
            min value
        :param max_x: float
            max value
        """
        self.figure.x_range = Range1d(start=min_x, end=max_x)

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        self.figure = figure(
            y_range=self.x_axis_data,
            x_range=(0, 250000),
            height=self.height,
            width=self.width,
            sizing_mode="scale_both",
            title="",
            tools=self.tools,
        )

        self.figure.hbar(
            y="categories",
            right="values",
            height=self.bar_height,
            fill_color=self.colors,
            source=self.source,
        )

        self.figure.toolbar.logo = None
        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label


class MeasurementBarScatterPlot(BarPlot):
    """
    2 Y axis plot (bar on th left, scatter on the right) class implementation
    """

    def __init__(
            self,
            primary_axis_name,
            primary_color,
            secondary_axis_name,
            secondary_axis_format,
            secondary_color,
            country=None,
            label=False,
            **params):
        """
        Constructor of BarScatterPlot class

        :param colors : str
            color of the bars
        :param params: inherited args
        """
        super().__init__(**params)
        self.primary_axis_name = primary_axis_name
        self.primary_color = primary_color
        self.secondary_axis_name = secondary_axis_name
        self.secondary_axis_format = secondary_axis_format
        self.secondary_color = secondary_color
        self.label = label
        self.country = country

        # Initialise hover tool
        if len(self.tooltips) > 0:
            self.hover = HoverTool(tooltips=self.tooltips)
            self.hover.mode = "vline"
            self.tools = [self.hover] + self.tools

        self.source = ColumnDataSource(data=dict(x=[], y=[], y1=[], y2=[], formatted_y=[], formatted_y2=[]))

        self.make_figure()
        self.panel = self.get_panel()

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        # Create plot
        self.figure = figure(
            x_range=self.x_axis_data,
            height=self.height,
            width=self.width,
            # tooltips=self.tooltips,
            sizing_mode="scale_both",
            tools=self.tools,
        )

        # Format the global plot
        self.figure.title.text = ""
        self.figure.y_range.start = 0
        self.figure.x_range.range_padding = 0
        self.figure.xaxis.major_label_text_font_style = "normal"
        self.figure.xgrid.grid_line_color = None
        self.figure.xaxis.axis_label = "Number of Impressions"

        # Format the left Y-axis
        self.figure.yaxis.minor_tick_line_color = None
        self.figure.yaxis.axis_label = self.primary_axis_name
        self.figure.yaxis.formatter = MSMT_SIMPLE_BARPLOT_FORMATTER
        self.figure.yaxis.axis_label_text_color = self.primary_color

        # Format the secondary Y-axis
        self.figure.extra_y_ranges = {
            "y2_name": Range1d(start=0, end=1)}
        y2_formatted = LinearAxis(y_range_name="y2_name", axis_label=self.secondary_axis_name,
                                  axis_label_text_color=self.secondary_color, minor_tick_line_color=None)

        currency = currency_mapper(self.country, 'local')[0]

        if self.secondary_axis_format == "percentage":
            y2_formatted.formatter = NumeralTickFormatter(format='0.0%')
        elif self.secondary_axis_format == "int":
            y2_formatted.formatter = SIMPLE_BARPLOT_FORMATTER
        elif self.secondary_axis_format == "monetary":
            y2_formatted.formatter = FuncTickFormatter(code=f"""
                                                 {{
                                                    var num =  (tick).toFixed(2)
                                                 }}
                                                 return `{currency}${{num}}`""")

        else:
            y2_formatted.formatter = NumeralTickFormatter(format='0.00')

        self.figure.add_layout(y2_formatted, 'right')

        # Add bar plot in the left Y-axis
        self.figure.vbar(
            x="x",
            top="y",
            source=self.source,
            width=0.7,
            line_color="White",
            fill_color=self.primary_color,
        )

        # Add scatter plot in the secondary Y-axis
        self.figure.square(x="x", y="y2", size=7, color=self.secondary_color, source=self.source,
                           y_range_name="y2_name")

        # Labels
        if self.label:
            labels = LabelSet(
                x="x",
                y="y",
                y1="y1",
                y2="y2",
                level="glyph",
                x_offset=-17.1,
                y_offset=-15,
                source=self.source,
                render_mode="canvas",
            )
            self.figure.add_layout(labels)

        self.figure.toolbar.logo = None

    def update_second_axis(self, min_y, max_y):
        """
        At each refresh, update x axis range values
        :param min_y: float
            min value
        :param max_y: float
            max value
        """
        self.figure.extra_y_ranges["y2_name"].start = min_y
        self.figure.extra_y_ranges["y2_name"].end = max_y


class HorizontalStackedBarPlot(BarPlot):
    """
    This Horizontal Bar plot works for percentage stacked plot (all bars are from 0 to 1)
    """

    def __init__(self, color1="#616161", color2="#bdbdbd", display_legend=False, **params):
        """
            Constructor of BasicBarPlot class

            :param colors : str
                color of the bars
            :param params: inherited args
            """
        super().__init__(**params)
        self.color1 = color1
        self.color2 = color2
        self.display_legend = display_legend

        self.source = ColumnDataSource(data=dict(y=[], x=[],
                                                 label_location_1=[], label_text_1=[],
                                                 label_location_2=[], label_text_2=[]))

        self.make_figure()
        self.panel = self.get_panel()

    def make_figure(self):
        """
            Make the figure using bokeh components and defined parameters
            """
        # Create plot
        self.figure = figure(
            y_range=self.x_axis_data,
            x_range=(0, 1),
            height=220,
            width=self.width,
            # tooltips=self.tooltips,
            sizing_mode="scale_both",
            y_axis_label="",
            tools=self.tools,
        )

        # Plot the first part of the bar
        if self.display_legend:
            self.figure.hbar(
                y="y",
                left=0,  # the bar starts at 0 and ends at the percentage value.
                right="x",
                source=self.source,
                height=0.85,
                line_color="White",
                fill_color=self.color1,
                legend_label="New shoppers"
            )
        else:
            self.figure.hbar(
                y="y",
                left=0,  # the bar starts at 0 and ends at the percentage value.
                right="x",
                source=self.source,
                height=0.85,
                line_color="White",
                fill_color=self.color1,
            )

        # Plot the second part of the bar
        if self.display_legend:
            self.figure.hbar(
                y="y",
                left="x",  # the bar starts at the x percentage value and ends at 100%.
                right=1,
                source=self.source,
                height=0.85,
                line_color="White",
                fill_color=self.color2,
                legend_label="Returning shoppers"
            )
        else:
            self.figure.hbar(
                y="y",
                left="x",  # the bar starts at the x percentage value and ends at 100%.
                right=1,
                source=self.source,
                height=0.85,
                line_color="White",
                fill_color=self.color2,
            )

        # Style the chart Title
        self.figure.title.text = ""
        self.figure.title.text_font_size = '14px'

        # Style the legend
        self.figure.legend.label_text_font_size = '10px'

        # Style the axis
        self.figure.outline_line_color = None
        self.figure.xaxis.visible = False
        self.figure.xgrid.grid_line_color = None
        self.figure.ygrid.grid_line_color = None
        self.figure.yaxis.minor_tick_line_color = None
        self.figure.xaxis.minor_tick_line_color = None
        self.figure.yaxis.major_tick_line_color = None
        self.figure.xaxis.major_tick_line_color = None
        self.figure.yaxis.axis_line_color = "#9e9e9e"

        # Short audience segment name if too long
        self.figure.yaxis.formatter = FuncTickFormatter(
            code="""
                        if (tick.length > 30) return tick.substring(0, 30) + '...';
                        else return tick;
                    """
        )

        # Add labels
        self.figure.text(
            x='label_location_1',
            y='y',
            text='label_text_1',
            text_align='center',
            text_baseline='middle',
            text_font_size='9px',
            source=self.source, )

        self.figure.text(
            x='label_location_2',
            y='y',
            text='label_text_2',
            text_align='center',
            text_baseline='middle',
            text_font_size='9px',
            source=self.source, )

        self.figure.toolbar.logo = None
