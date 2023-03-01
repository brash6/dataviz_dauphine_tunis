import panel as pn
import param
from bokeh.models.formatters import PrintfTickFormatter
from google.cloud import bigquery

from TP4.modules.configurations_pane.configuration_pane import ConfigurationPane
from TP4.utils.gcp import (
    delete_tables,
    get_configurations,
    read_gbq_gcp,
    save_configurations,
)
from TP4.utils.notifications import error_notification, success_notification


class LoadConfigurations(ConfigurationPane):

    def __init__(self, **params):
        super().__init__(**params)

    @param.depends("load_button", watch=True)
    def get_configuration_from_table(self):
        selected_conf = self.saved_configurations
        df_configurations = self.configurations[self.configurations["configuration_name"]==selected_conf]
        print(df_configurations)

        return df_configurations

    def make_figure(self):
        self.saved_configurations_panel = pn.Param(self,
                                          name="",
                                          parameters=["saved_configurations"],
                                          widgets={
                                              "saved_configurations": pn.widgets.Select(align='center')})

        self.load_button_panel = pn.Param(self,
                                           name="",
                                           parameters=["load_button"],
                                           widgets={
                                               "load_button": pn.widgets.Button(name='Load Configuration',
                                                                         max_width=150,
                                                                         align='center')})

        self.panel = pn.Row(self.saved_configurations_panel, self.load_button_panel)
