import panel as pn

from TP4.modules.base.base_selector import BaseSelector
from TP4.pages.example_dashboards.plotting_high_dimensional_data.queries import BQClient


class VGSelector(BaseSelector):

    def __init__(self, BQHandler: BQClient, **params):
        self.BQHandler = BQHandler
        super().__init__(**params)

        self.settings_panel = pn.Row()
