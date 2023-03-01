import panel as pn
import param
from panel.io.loading import start_loading_spinner, stop_loading_spinner

from TP4.modules.base.base_plot import BasePlot
from TP4.utils.gcp import get_configurations, save_configurations


class ConfigurationPane(param.Parameterized):

    saved_configurations = param.Selector()
    new_configuration = param.String()
    save_button = param.Action(lambda x: x.param.trigger("save_button"), label="Save Configuration")
    load_button = param.Action(lambda x: x.param.trigger("load_button"), label="Load Configuration")
    delete_button = param.Action(lambda x: x.param.trigger("delete_button"), label="Delete Configuration")
    loading = param.Boolean(default=False, doc="Whether or not to show the spinner")


    def __init__(self, config_table, tenant_id, schema, **params):
        super().__init__(**params)
        self.config_table = config_table
        self.tenant_id = tenant_id
        self.schema = schema
        self.configurations = get_configurations(self.config_table, self.tenant_id, self.schema)
        self.make_figure()
        if self.configurations is not None:
            print("updating the saved configurations list")
            print(self.configurations["configuration_name"].unique())
            self.param.saved_configurations.objects = self.configurations["configuration_name"].unique()
            with param.discard_events(self):
                if len(self.configurations["configuration_name"].unique()) > 0:
                    self.saved_configurations = list(self.configurations["configuration_name"].unique())[0]

    @param.depends("loading", watch=True)
    def _update_loading_spinner(self):
        """
        Function to start and stop the loading spinner relevantly
        """
        if self.loading:
            start_loading_spinner(self.panel)
        else:
            stop_loading_spinner(self.panel)

    def update_configurations_list(self):
        raise

    def get_configuration_dict(self):
        raise

    def save_configuration(self):
        raise

    def make_figure(self):
        raise
