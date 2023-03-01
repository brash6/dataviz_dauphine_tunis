import math

import panel as pn
from matplotlib.figure import Figure

from TP4.modules import BarPlot


class RadarPlot(BarPlot):
    """

    In Dashboard :
    # Radar Plot

    self.fig0 = Figure(figsize=(7, 6))

    self.mpl_pane = pn.pane.Matplotlib(self.fig0, dpi=100)

    self.radar_plot = RadarPlot(
                                mpl_pane=self.mpl_pane
                                )

    """

    def __init__(self, mpl_pane, **params):

        super().__init__(**params, x_axis_data='', title='')
        self.mpl_pane = mpl_pane

    def update_data(self, df, labels_radar, colors):

        self.fig0 = Figure(figsize=(7, 6))
        self.ax = self.fig0.add_subplot(111, polar=True)

        # number of variable
        categories = list(df)[1:]
        N = len(categories)

        # Initialise the spider plot

        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * math.pi for n in range(N)]
        angles += angles[:1]

        # If you want the first axis to be on top:
        self.ax.set_theta_offset(math.pi / 2)
        self.ax.set_theta_direction(-1)

        # Draw one axe per variable + add labels
        self.ax.set_xticks(angles[:-1], categories)

        # Draw ylabels
        self.ax.set_rlabel_position(0)

        # ------- PART 2: Add plots

        # Plot each individual = each line of the data
        # I don't make a loop, because plotting more than 3 groups makes the chart unreadable

        for i in range(len(labels_radar)):
            values = df.loc[i].drop('group').values.flatten().tolist()
            values += values[:1]
            self.ax.plot(angles, values, linewidth=1, linestyle='solid', label=labels_radar[i])
            self.ax.fill(angles, values, colors[i], alpha=0.1)

        # Legend
        self.fig0.legend(loc='upper right')
        self.mpl_pane.object = self.fig0
