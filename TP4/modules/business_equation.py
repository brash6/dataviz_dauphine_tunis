import math

from bokeh.models import Label, Rect, Segment
from bokeh.plotting import figure

from TP4.modules.base.base_plot import BasePlot


class BusinessEquation(BasePlot):
    """
    Class implementation of the BusinessEquation plot primitive
    """

    def __init__(self, title, height=600, width=1200, **params):
        """
        Constructor of the BusinessEquation plot, uses hardcoded data for initialisation
        :param title: str
            title of the plot
        :param height: int
            height of the plot, default 600
        :param width: int
            width of the plot, default 1200
        :param params: inherited args
        """
        super().__init__(**params)
        self.title = title
        self.height = height
        self.width = width
        self.data_bizeq = []
        self.data_bizeq.append(["Value Sales", "284K€", "up", "+1.14%", "+17.82K€"])
        self.data_bizeq.append(["Trips", "132K", "up", "+0.71%", "+1.2K"])
        self.data_bizeq.append(["Average Order", "14.5€", "down", "-0.06%", "-0.6€"])
        self.data_bizeq.append(["# Shoppers", "1.4M", "down", "-0.02%", "-0.2K"])
        self.data_bizeq.append(["Frequency", "2.7", "up", "+3.1%", "+0.05"])
        self.data_bizeq.append(["Average Price", "1.92€", "up", "+1.2%", "+0.17€"])
        self.data_bizeq.append(["Basket Size", "48.3€", "up", "+1.9%", "+2.12€"])
        self.data_bizeq.append(["Traffic", "245K", "up", "+1.51%", "+6.21K"])
        self.data_bizeq.append(["Conversion", "2.31%", "down", "-0.01%", "-0.02%"])

        self.make_figure()
        self.panel = self.get_panel()

    def set_box_equation(self, box_x, box_y, title, big_sum, tri, change, abs_change):
        self.figure.add_layout(
            Label(x=box_x, y=box_y - 15, text_align="center", text=title, text_font_style="bold")
        )
        self.figure.add_layout(
            Label(
                x=box_x,
                y=box_y - 35,
                text_align="center",
                text=big_sum,
                text_font_size="20pt",
                text_font_style="bold",
            )
        )
        if tri == "up":
            self.figure.triangle(
                box_x - 20, box_y - 50, size=20, color="green", angle=math.radians(0)
            )
        elif tri == "down":
            self.figure.triangle(
                box_x - 20, box_y - 47, size=20, color="red", angle=math.radians(180)
            )
        else:
            pass
        self.figure.add_layout(
            Label(
                x=box_x - 16,
                y=box_y - 53,
                text_align="left",
                text=change,
                text_font_size="14pt",
                text_font_style="bold",
                text_color="black",
            )
        )
        self.figure.add_layout(
            Label(
                x=box_x + 20,
                y=box_y - 52,
                text_align="right",
                text=abs_change,
                text_font_size="12pt",
                text_font_style="bold",
                text_color="green" if tri == "up" else "red",
            )
        )

    def create_graph(self, box_pos, data_bizeq):
        self.box_pos = box_pos
        self.data_bizeq = data_bizeq
        for item in range(0, len(self.box_pos)):
            self.set_box_equation(
                self.box_pos[item][0],
                self.box_pos[item][1],
                self.data_bizeq[item][0],
                self.data_bizeq[item][1],
                self.data_bizeq[item][2],
                self.data_bizeq[item][3],
                self.data_bizeq[item][4],
            )

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
            y_range=(0, 500),
        )
        pos_x = 0
        top = 499
        box_width = 50
        box_height = 60
        height_between_box = 40  # distance between bottom of top box and top of below box
        width_between_box = 200  # distance between right of left box and left of right box
        affaiblissement = 140
        depth = 3

        pos_x_level = [[pos_x]]

        for level in range(1, depth + 1):
            items = []
            for previous in range(0, len(pos_x_level[level - 1])):
                val = pos_x_level[level - 1][previous]
                items.append(val - width_between_box / 2)
                items.append(val + width_between_box / 2)
            pos_x_level.append(items)
            width_between_box = width_between_box - affaiblissement

        width_between_box = 200  # distance between right of left box and left of right box

        self.box_pos = []

        # Levels
        self.figure.add_glyph(
            Rect(
                x=pos_x,
                y=top - box_height / 2,
                width=box_width,
                height=box_height,
                line_color="black",
                fill_color=None,
            )
        )
        self.box_pos.append((pos_x, top - 1))
        self.figure.add_glyph(
            Segment(
                x0=pos_x,
                y0=top - box_height,
                x1=pos_x,
                y1=top - box_height - height_between_box / 2,
                line_color="black",
                line_width=1,
            )
        )

        hz_exclusion = [(3, 1), (3, 2), (3, 3)]
        vt_exclusion = [(3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7)]
        end_box_exclusion = [(2, 1), (2, 2), (2, 3)]

        for level in range(1, depth + 1):
            # Horizontal
            for hz in range(0, 2 ** (level - 1)):
                if (level, hz) in hz_exclusion:
                    pass
                else:
                    self.figure.add_glyph(
                        Segment(
                            x0=pos_x_level[level][2 * hz],
                            y0=top
                            - level * (box_height + height_between_box)
                            + height_between_box / 2,
                            x1=pos_x_level[level][2 * hz + 1],
                            y1=top
                            - level * (box_height + height_between_box)
                            + height_between_box / 2,
                            line_color="black",
                            line_width=1,
                        )
                    )
            # Verticals
            for vt in range(0, 2 ** (level)):
                if (level, vt) in vt_exclusion:
                    pass
                else:
                    self.figure.add_glyph(
                        Segment(
                            x0=pos_x_level[level][vt],
                            y0=top
                            - level * (box_height + height_between_box)
                            + height_between_box / 2,
                            x1=pos_x_level[level][vt],
                            y1=top - level * (box_height + height_between_box),
                            line_color="black",
                            line_width=1,
                        )
                    )
                    # Next Boxes
                    self.figure.add_glyph(
                        Rect(
                            x=pos_x_level[level][vt],
                            y=top - level * (box_height + height_between_box) - box_height / 2,
                            width=box_width,
                            height=box_height,
                            line_color="black",
                            fill_color=None,
                        )
                    )
                    self.box_pos.append(
                        (pos_x_level[level][vt], top - level * (box_height + height_between_box))
                    )
                    if level < depth:
                        if (level, vt) in end_box_exclusion:
                            pass
                        else:
                            self.figure.add_glyph(
                                Segment(
                                    x0=pos_x_level[level][vt],
                                    y0=top - level * (box_height + height_between_box) - box_height,
                                    x1=pos_x_level[level][vt],
                                    y1=top
                                    - (level + 1) * (box_height + height_between_box)
                                    + height_between_box / 2,
                                    line_color="black",
                                    line_width=1,
                                )
                            )

        self.create_graph(self.box_pos, self.data_bizeq)

        self.figure.xaxis.visible = False
        self.figure.yaxis.visible = False
        self.figure.xgrid.visible = False
        self.figure.ygrid.visible = False
        self.figure.outline_line_color = None
