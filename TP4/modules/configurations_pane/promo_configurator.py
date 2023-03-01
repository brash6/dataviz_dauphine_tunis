import pandas as pd
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
from TP4.utils.notifications import (
    error_notification,
    info_notification,
    success_notification,
)


class PromoConfigurator(ConfigurationPane):
    min_sales_volume = param.Integer(1)
    min_sales_value = param.Number(18)
    method = param.Selector(default='Mean')
    nb_months = param.Selector(default="3")
    avg_period_threshold = param.Number(0.1)
    zscore = param.Integer(3)
    window_align = param.Boolean(False)
    io = param.Boolean(False)


    def __init__(self, currency_symbol, **params):
        self.currency_symbol = currency_symbol
        super().__init__(**params)

    def update_configurations_list(self):
        # return True
        print(self.configurations["configuration_name"].unique())
        print("updating the saved configurations list")
        if len(self.configurations["configuration_name"].unique()) > 0:
            self.param.saved_configurations.objects = list(self.configurations["configuration_name"].unique())
            self.saved_configurations = list(self.configurations["configuration_name"].unique())[0]
        else:
            print("trying to update list of conf")
            self.saved_configurations_panel.widgets["saved_configurations"].options = list(self.configurations["configuration_name"].unique())

    def check_if_config_name_exists(self, config_name):
        for name in list(self.configurations["configuration_name"].unique()):
            if name == config_name:
                return True
            else:
                return False

    @param.depends("save_button", watch=True)
    def save_configuration(self):
        print("saving config")
        self.loading = True
        if len(self.new_configuration) > 0:
            if self.check_if_config_name_exists(self.new_configuration):
                info_notification("This configuration name already exists, let's overwrite it")
                df_configurations = self.configurations[self.configurations["configuration_name"] != self.new_configuration]
                current_config = pd.DataFrame(self.get_configuration_dict(), index=[0])
                self.configurations = pd.concat([df_configurations, current_config], ignore_index=True)
                self.configurations.to_gbq(destination_table=self.config_table, if_exists="replace")
                print(self.configurations)
                success_notification("Configuration has been saved")
            else:
                info_notification("Saving new configuration")
                save_configurations(self.config_table, self.get_configuration_dict())
                self.configurations = get_configurations(self.config_table, self.tenant_id, self.schema)
                self.update_configurations_list()
                success_notification("Config has been saved")
        else:
            error_notification("Configuration name should be set")
        self.loading = False

    def get_configuration_dict(self):
        dict_current_config = {"configuration_name": str(self.new_configuration),
                 "tenant_id": str(self.tenant_id),
                 "min_sales_volume": self.min_sales_volume,
                 "min_sales_value": float(self.min_sales_value),
                 "method": str(self.method),
                 "nb_months": int(self.nb_months),
                 "avg_period_threshold": self.avg_period_threshold,
                 "window_align": self.window_align,
                 "io": self.io,
                 "zscore": self.zscore}
        return dict_current_config

    def set_config_from_table(self, df_configurations):
        print("CONFIG SETTING UP")
        self.set_param("min_sales_volume", int(df_configurations["min_sales_volume"].values[0]))
        self.set_param("min_sales_value", df_configurations["min_sales_value"].values[0])
        self.min_sales_value_panel.widgets["min_sales_value"].value = float(df_configurations["min_sales_value"].values[0])
        self.set_param("method", str(df_configurations["method"].values[0]))
        self.set_param("nb_months", str(df_configurations["nb_months"].values[0]))
        self.set_param("avg_period_threshold", df_configurations["avg_period_threshold"].values[0])
        self.set_param("window_align", bool(df_configurations["window_align"].values[0]))
        self.window_align_panel.widgets["window_align"].value = bool(df_configurations["window_align"].values[0])
        self.set_param("io", bool(df_configurations["io"].values[0]))
        self.io_panel.widgets["io"].value = bool(df_configurations["io"].values[0])
        self.set_param("zscore", int(df_configurations["zscore"].values[0]))

    @param.depends("load_button", watch=True)
    def get_configuration_from_table(self):
        selected_conf = self.saved_configurations
        df_configurations = self.configurations[self.configurations["configuration_name"]==selected_conf]
        print(df_configurations)
        if not df_configurations.empty:
            self.set_config_from_table(df_configurations)
        else:
            error_notification("No configuration stored")

    @param.depends("delete_button", watch=True)
    def delete_configuration_from_table(self):
        self.loading=True
        selected_conf = self.saved_configurations
        df_configurations = self.configurations[self.configurations["configuration_name"]!=selected_conf]
        print(df_configurations)
        df_configurations.to_gbq(destination_table=self.config_table, if_exists="replace")
        self.configurations = get_configurations(self.config_table, self.tenant_id, self.schema)
        print(self.configurations)
        self.update_configurations_list()
        self.loading=False

    def make_figure(self):
        self.new_configuration_panel = pn.Param(self,
                                                name="",
                                                parameters=["new_configuration"],
                                                widgets={
                                                    "new_configuration": pn.widgets.TextInput(placeholder='New Configuration Name',
                                                                                              align='center')})
        self.save_button_panel = pn.Param(self,
                                          name="",
                                          parameters=["save_button"],
                                          widgets={
                                              "save_button": pn.widgets.Button(name='Save Configuration',
                                                                                 max_width=150,
                                                                                 align='center')})
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

        self.delete_button_panel = pn.Param(self,
                                          name="",
                                          parameters=["delete_button"],
                                          widgets={
                                              "delete_button": pn.widgets.Button(name='Delete Configuration',
                                                                               max_width=150,
                                                                               align='center')})

        self.method_panel = pn.Param(self,
                                      name="",
                                      parameters=["method"],
                                      widgets={
                                          "method": pn.widgets.Select(name="Price Benchmark Aggregation",
                                                 options=['Mean', 'Median', 'Quantile75', 'Second highest'],
                                                 value='Mean',
                                                 max_width=350,
                                                 align='center')})


        self.nb_months_panel = pn.Param(self,
                                     name="",
                                     parameters=["nb_months"],
                                     widgets={
                                         "nb_months": pn.widgets.Select(name="Nb of Months (window size)",
                                                    options=["1", "2", "3", "4", "5", "6", "12", "18", "24"],
                                                    value="3",
                                                    max_width=350,
                                                    align='center')})

        self.window_align_panel = pn.Param(self,
                                        name="",
                                        parameters=["window_align"],
                                        widgets={
                                            "window_align": pn.widgets.Checkbox(name="Period Align Center", active=[],
                                               max_width=350,
                                               align='center')})

        self.io_panel = pn.Param(self,
                                   name="",
                                   parameters=["io"],
                                   widgets={
                                       "io": pn.widgets.Checkbox(name="In/Out Product Detector",
                                                                           active=[],
                                                                           max_width=350,
                                                                           align='center')})

        self.min_sales_volume_panel = pn.Param(self,
                                 name="",
                                 parameters=["min_sales_volume"],
                                 widgets={
                                     "min_sales_volume": pn.widgets.IntSlider(start=0, end=100, value=0, step=1,
                                                     name="Minimum Daily Volume Threshold",
                                                     max_width=310,
                                                     align='center')})

        self.zscore_panel = pn.Param(self,
                                       name="",
                                       parameters=["zscore"],
                                       widgets={
                                           "zscore": pn.widgets.IntSlider(start=0, end=6, value=3, step=1,
                                                                          name="Z-Score Value",
                                                                          disabled=True,
                                                                          max_width=350,
                                                                          align='center')})

        self.min_sales_value_panel = pn.Param(self,
                                               name="",
                                               parameters=["min_sales_value"],
                                               widgets={
                                                   "min_sales_value": pn.widgets.FloatSlider(start=0, end=100, value=0, step=1,
                                                             name="Minimum Daily Value Threshold",
                                                             format=PrintfTickFormatter(format=f"""%.2f {self.currency_symbol}"""),
                                                             max_width=310,
                                                             align='center')})

        self.avg_period_threshold_panel = pn.Param(self,
                                               name="",
                                               parameters=["avg_period_threshold"],
                                               widgets={
                                                   "avg_period_threshold": pn.widgets.FloatSlider(start=0, end=1.0, value=0.1, step=0.05,
                                                                    name="Discount Threshold(⋊)",
                                                                    max_width=350,
                                                                    align='center')})

        gspec = pn.GridSpec(sizing_mode='stretch_both', width=900, height=400)

        gspec[0, 0] = self.new_configuration_panel
        gspec[0, 1] = self.save_button_panel
        gspec[1, 0] = self.saved_configurations_panel
        gspec[1, 1] = self.load_button_panel
        gspec[1, 2] = self.delete_button_panel

        gspec[2, 0] = self.method_panel
        gspec[2, 1] = self.nb_months_panel
        gspec[2, 2] = self.window_align_panel
        gspec[2, 3] = self.avg_period_threshold_panel

        gspec[3, 0] = self.min_sales_value_panel
        gspec[3, 1] = self.min_sales_volume_panel
        gspec[3, 2] = self.io_panel
        gspec[3, 3] = self.zscore_panel

        self.panel = gspec
