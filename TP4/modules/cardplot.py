import math

from bokeh.models import ColumnDataSource, Label, Rect
from bokeh.plotting import figure

from TP4.constants.constants import LR_DIVERGING_COLORS
from TP4.modules.base.base_plot import BasePlot
from TP4.utils.formatters import format_number_to_string


class CardPlot(BasePlot):
    """
    Class implementation of the CardPlot primitive
    """

    def __init__(
        self,
        title,
        value_text,
        variation_value=None,
        to_compare_text="",
        height=200,
        width=500,
        **params
    ):
        """
        Constructor of the CardPlot
        :param title: str
            title of the plot
        :param value_text: str
            Value to print at the center of the card
        :param variation_value: float, optional, default None
            Value which represents the variation of the value compared with any wanted value
        :param to_compare_text: str, optional, default ""
            Text related to the variation value
        :param height: int, default 200
            height of the plot
        :param width: int, default 500
            width of the plot
        :param params: inherited args
        """
        super().__init__(**params)
        self.title = title
        self.value_text = value_text
        self.variation_value = variation_value
        self.to_compare_text = to_compare_text
        self.height = height
        self.width = width
        self.source = ColumnDataSource(
            data=dict(triangle_y=[], triangle_angle=[], triangle_color=[])
        )

        self.make_figure()
        self.panel = self.get_panel()

    def update_card(self, value_text, variation_value=None, to_compare_text=""):
        """
        At each refresh, update the cardplot with new value_text, variation_value and to_compare_text
        :param value_text: str
            Value to print at the center of the card
        :param variation_value: float, optional, default None
            Value which represents the variation of the value compared with any wanted value
        :param to_compare_text: str, optional, default ""
            Text related to the variation value
        """
        self.value_text = value_text
        self.displayed_value.text = self.value_text
        self.variation_value = variation_value
        self.to_compare_text = to_compare_text
        if self.variation_value is not None:
            self.diplayed_value_comp.text = (
                str(self.variation_value) + " " + self.to_compare_text
            )
            if self.variation_value > 0:
                self.source.data["triangle_y"] = [280]
                self.source.data["triangle_angle"] = [math.radians(0)]
                self.source.data["triangle_color"] = ["green"]
            else:
                self.source.data["triangle_y"] = [280]
                self.source.data["triangle_angle"] = [math.radians(180)]
                self.source.data["triangle_color"] = ["red"]

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        self.figure = figure(
            plot_width=self.width,
            plot_height=self.width,
            title=self.title,
            toolbar_location=None,
            x_range=(-200, 200),
        )
        self.figure.add_glyph(
            Rect(x=0, y=300, width=300, height=80, line_color="black", fill_color=None)
        )
        self.figure.add_layout(
            Label(
                x=0,
                y=320,
                text_align="center",
                text=self.title,
                text_font_size="12pt",
                text_font_style="bold",
                text_color="black",
            )
        )
        self.displayed_value = Label(
            x=0,
            y=295,
            text_align="center",
            text=self.value_text,
            text_font_size="25pt",
            text_font_style="bold",
            text_color="black",
        )
        self.figure.add_layout(self.displayed_value)
        if self.variation_value is not None:
            self.figure.triangle(
                x=-40,
                y="triangle_y",
                size=25,
                color="triangle_color",
                angle="triangle_angle",
                source=self.source,
            )
            self.diplayed_value_comp = Label(
                x=-20,
                y=278,
                text_align="left",
                text=str(self.variation_value) + " " + self.to_compare_text,
                text_font_size="12pt",
                text_font_style="normal",
                text_color="black",
            )
            self.figure.add_layout(self.diplayed_value_comp)

        self.figure.xaxis.visible = False
        self.figure.yaxis.visible = False
        self.figure.xgrid.visible = False
        self.figure.ygrid.visible = False
        self.figure.outline_line_color = None


class MeasurementCardPlot(BasePlot):
    """
    Class implementation of the Measurement CardPlot primitive
    """

    def __init__(
            self,
            title,
            value_text,
            text,
            value_format=None,
            secondary_value=None,
            secondary_value_format=None,
            to_compare_text="",
            height=250,
            width=500,
            **params
    ):
        """
        Constructor of the CardPlot
        :param title: str
            title of the plot
        :param value_text: str
            Value to print at the center of the card
        :param secondary_value: float, optional, default None
            Value which represents the secondary of the value compared with any wanted value
        :param to_compare_text: str, optional, default ""
            Text related to the secondary value
        :param icon: bol
            True if a red/green icon is need
        :param height: int, default 300
            height of the plot
        :param width: int, default 500
            width of the plot
        :param params: inherited args
        """
        super().__init__(**params)
        self.title = title
        self.value_text = value_text
        self.value_format = value_format
        self.text = text
        self.secondary_value = secondary_value
        self.secondary_value_format = secondary_value_format
        self.to_compare_text = to_compare_text
        self.height = height
        self.width = width

        self.make_figure()
        self.figure.toolbar.active_drag = None
        self.panel = self.get_panel()

    def update_card(self, value, country=None, value_format=None, secondary_value=None, secondary_value_format=None, to_compare_text="", background_color=None):
        """
        At each refresh, update the cardplot with new value_text, secondary_value and to_compare_text
        :param value: str
            Value to print at the center of the card
        :param country: str
            CPG country, used to display the relevant currency
        :param value_format: str
            String to format the value. Possible values are: None, 'monetary', 'percentage', 'number', 'decimal', 'monetary_dec'
        :param secondary_value: float, optional, default None
            Value which represents the secondary value compared with any wanted value
        :param secondary_value_format: string, optional, default None
            String to format the value. Possible values are: None, 'monetary', 'percentage', 'number', 'decimal', 'monetary_dec'
        :param to_compare_text: str, optional, default ""
            Text related to the secondary value
        :param background_color: str, optional, default None
            background color used
        """

        self.figure.add_glyph(
            Rect(x=0, y=300, width=400, height=80, line_color=background_color, fill_color=background_color)
        )
        self.figure.background_fill_color=background_color

        self.value_text = format_number_to_string(value, value_format, country)

        self.displayed_value.text = self.value_text

        # For readability reasons white color is used for a non white background
        if background_color in [LR_DIVERGING_COLORS[0], LR_DIVERGING_COLORS[1]]:
            self.displayed_value.text_color = "white"
            self.title_text.text_color = "white"
        elif background_color in [LR_DIVERGING_COLORS[2]]:
            self.displayed_value.text_color = "#212121"
            self.title_text.text_color = "#212121"
        else:
            self.displayed_value.text_color = "#212121"
            self.title_text.text_color = "#BDBDBD"

        if self.secondary_value is not None:

            self.secondary_value = format_number_to_string(secondary_value, secondary_value_format, country)

            self.to_compare_text = to_compare_text

            # Concatenate the field to display
            self.diplayed_value_comp.text = (
                    str(self.secondary_value) + " " + self.to_compare_text
            )
            if background_color in [LR_DIVERGING_COLORS[0], LR_DIVERGING_COLORS[1]]:
                self.diplayed_value_comp.text_color = "white"
            elif background_color in [LR_DIVERGING_COLORS[2]]:
                self.diplayed_value_comp.text_color = "#212121"
            else:
                self.diplayed_value_comp.text_color = "#BDBDBD"

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        self.figure = figure(
            plot_width=self.width,
            plot_height=self.height,
            toolbar_location=None,
            x_range=(-200, 200),
        )

        self.title_text = Label(
                x=0,
                y=285,
                text_align="center",
                text=self.text,
                text_font_size="12pt",
                text_font_style="normal",
                text_color="#BDBDBD",
            )
        self.figure.add_layout(self.title_text)

        self.displayed_value = Label(
            x=0,
            y=295,
            text_align="center",
            text=self.value_text,
            text_font_size="35pt",
            text_font_style="normal",
            text_color="#BDBDBD",
        )

        self.figure.add_layout(self.displayed_value)

        if self.secondary_value is not None:
            self.diplayed_value_comp = Label(
                x=0,
                y=270,
                text_align="center",
                text=str(self.secondary_value) + " " + self.to_compare_text,
                text_font_size="12pt",
                text_font_style="normal",
                text_color="#BDBDBD",
            )
            self.figure.add_layout(self.diplayed_value_comp)

        self.figure.xaxis.visible = False
        self.figure.yaxis.visible = False
        self.figure.xgrid.visible = False
        self.figure.ygrid.visible = False
        self.figure.outline_line_color = None
