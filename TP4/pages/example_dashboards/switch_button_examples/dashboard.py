import holoviews as hv
import panel as pn
import param
from bokeh.models import BoxSelectTool, BoxZoomTool, ResetTool, TapTool

from TP4.constants.constants import LR_SINGULAR_COLOR
from TP4.modules.barplots.simple_barplot import SimpleBarPlot
from TP4.modules.base.base_dashboard import BaseExampleDashboard
from TP4.modules.panel_text import PanelText
from TP4.pages.example_dashboards.switch_button_examples.queries import BQClient
from TP4.pages.example_dashboards.switch_button_examples.selector import (
    VGSelector,
)
from TP4.utils.view import get_template
from TP4.awesome_panel_extensions.site import site

hv.extension("bokeh")

APPLICATION = site.create_application(
    url="switch_button_examples",
    name="Switch Data Button Examples",
    tags=["UX"],
    folder="example_dashboards"
)


class Dashboard(BaseExampleDashboard):
    # Declare here the used selector
    selector = param.ClassSelector(class_=VGSelector)
    switch_region_button = param.ObjectSelector(default='Global')

    # Doesn't change, used to instantiate all the plots to render using Panel
    panels = param.List()

    @param.depends("switch_region_button", watch=True, on_init=False)
    def widget_event_handler(self):
        if not self.first:
            self.update_plot(self.loaded_data)

    def __init__(self, BQHandler: BQClient, **params):
        super().__init__(**params)
        self.BQHandler = BQHandler

        # Create a selector
        self.selector = VGSelector(self.BQHandler)

        # Create Plots
        self.plot_text = PanelText(text="""
        Here are some examples of plots updatable using a switch data button.
        The data used is an open-source dataset of video games sales that can be found [here](https://www.kaggle.com/gregorut/videogamesales).
        """, about=True)

        self.switch_region_button_panel = pn.Param(
            self,
            name="",
            parameters=["switch_region_button"],
            widgets={"switch_region_button": pn.widgets.RadioButtonGroup(name='switch_region_button', value='Global',
                                                                options=['Global', 'Japan', 'Europe', "North America"],
                                                                width=150, align='center')})

        # Simple BarPlot
        self.sales_by_platform_region = SimpleBarPlot(
            x_axis_data=["i"],
            x_axis_label="platform",
            y_axis_label="sales (in M€)",
            title="Simple BarPlot : Video games sales per platform",
            colors=LR_SINGULAR_COLOR,
            tools=[BoxSelectTool(), ResetTool(), TapTool(), BoxZoomTool()],
            tooltips="""
                     <b>Platform : </b> @x <br>
                     <b>Sales : </b> @y{(0.0 a)}€
                     """,
        )

        # Add in the panels list all the declared plot figures
        self.panels = [
            self.plot_text.panel,
            pn.Row(pn.Column(self.switch_region_button_panel, margin=(0, 10, 0, 10)),
                   pn.Column('', max_width=100)),
            self.sales_by_platform_region.panel,
        ]

        # Doesn't change
        self.settings_panel = self.get_settings_panel()
        self.main = pn.Column(*self.panels, sizing_mode="stretch_both")

        self.view = pn.Row(self.main, self.settings_panel)

    def get_data(self, filters):
        print("getting data")

        data = self.BQHandler.query_sales_by_platform(filters)
        data2 = self.BQHandler.query_sales_per_year(filters)

        self.loaded_data = [data, data2]

        return [data, data2]

    def update_plot(self, data):
        print("update")
        data2 = data[1]
        data = data[0]

        self.sales_by_platform_region.figure.x_range.factors = list(data["platform"])

        if self.switch_region_button == 'Global':
            self.sales_by_platform_region.source.data = dict(
                x=list(data["platform"]),
                y=list(data["sales"]),
            )
        if self.switch_region_button == 'Japan':
            self.sales_by_platform_region.source.data = dict(
                x=list(data["platform"]),
                y=list(data["jp_sales"]),
            )
        if self.switch_region_button == 'Europe':
            self.sales_by_platform_region.source.data = dict(
                x=list(data["platform"]),
                y=list(data["eu_sales"]),
            )
        if self.switch_region_button == 'North America':
            self.sales_by_platform_region.source.data = dict(
                x=list(data["platform"]),
                y=list(data["na_sales"]),
            )

    def get_user_filters(self):
        return False

    def get_settings_panel(self):
        settings_panel = pn.Column(
            pn.Param(self, parameters=["refresh_data"],
                     widgets={
                         "refresh_data": {"type": pn.widgets.Button(name='REFRESH DATA', button_type="success" )}
                     }),
            self.selector.settings_panel)
        return settings_panel


@site.add(APPLICATION)
def view():
    return get_template(BQClient, Dashboard, name_tab="Switch Data Button Examples")


if __name__.startswith("bokeh"):
    view().servable()
