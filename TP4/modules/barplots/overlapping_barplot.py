import math

from bokeh.models import ColumnDataSource, HoverTool, LabelSet, Rect
from bokeh.plotting import figure

from TP4.modules.barplots.base_barplot import BarPlot
from TP4.utils.formatters import NEW_Y_AXIS_FORMATTER, format_label


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
        self.glyph = Rect(x="x", y="rect_center", width='rect_width', height="back",
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
        self.figure.outline_line_color = None
        self.figure.yaxis.formatter = NEW_Y_AXIS_FORMATTER
        if len(self.x_axis_label) > 0:
            self.figure.xaxis.axis_label = self.x_axis_label
        if len(self.y_axis_label) > 0:
            self.figure.yaxis.axis_label = self.y_axis_label
        self.figure.toolbar.logo = None
