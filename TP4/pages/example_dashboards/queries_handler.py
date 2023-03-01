import holoviews as hv
import pandas as pd
import panel as pn
import param
from bokeh.sampledata.autompg import autompg_clean
from bokeh.sampledata.iris import flowers
from bokeh.sampledata.population import data
from logzero import logger

from TP4.constants.constants import ABT_DATASET
from TP4.template import FastDefaultTheme, LiverampTemplate
from TP4.awesome_panel_extensions.site import site
from explore_sql.queries import get_all_tables_from_dataset, get_df_query

hv.extension("bokeh")

APPLICATION = site.create_application(
    url="queries",
    name="Handle queries",
    tags=["UX"],
    folder="example_dashboards"
)

list_dataset = [f"{ABT_DATASET}_{i}" for i in ["wh", "work", "ai"]]


class ReactiveTables(param.Parameterized):
    dataset = param.ObjectSelector(default=f"{ABT_DATASET}_work", objects=list_dataset)
    table = param.ObjectSelector(default="default")
    rows = param.Integer(default=10, bounds=(0, 19))
    query = param.String()
    run_query = param.Action(label="RUN QUERY", doc="Update the plot")
    data = param.DataFrame(default=pd.DataFrame({"x": ["a", "b"], "y": ["c", "d"]}))

    def __init__(self, **params):
        super().__init__(**params)

        self.run_query = self.get_data
        self.main = pn.Column("## Query",
                              pn.Param(self,
                                       parameters=["query"]
                                       ),

                              pn.Param(
                                  self.param.run_query,
                                  widgets={"run_query": {"button_type": "primary"}},
                              ),
                              "## Description",
                              self.summary,
                              "## Table", self.table_plot, min_height=1000)
        self.settings_panel = pn.Column(
            pn.pane.Markdown("## Dataset"),
            pn.Param(self, parameters=["dataset", "table"],
                     )
        )

    def get_data(self, *_):
        try:
            df = get_df_query(self.query)
            self.data = df
            print("updated data")
        except:
            pass
        return True

    @param.depends('data')
    def summary(self):
        return self.data.describe()

    @param.depends('data')
    def table_plot(self):
        return self.data

    @param.depends('dataset', watch=True)
    def tables(self):
        list_tables = get_all_tables_from_dataset(self.dataset)
        self.param.table.objects = list_tables
        self.table = list_tables[0]
        self.query = f"select * from {self.dataset}.{self.table} limit 10"
        return list_tables

    @param.depends("table", watch=True)
    def write_query(self):
        self.query = f"select * from {self.dataset}.{self.table} limit 100"


@site.add(APPLICATION)
def view():
    pn.config.sizing_mode = "stretch_width"
    logger.info("getting the tenant")
    logger.info("getting the bqhandler")

    # Modify the name and the title of the dashboard
    logger.info("getting the app")
    app = ReactiveTables()
    logger.info("starting the layout")
    template = LiverampTemplate(title="Sales Overview",
                                theme=FastDefaultTheme,
                                header_background="#7ecb6f", font='Open Sans', accent_base_color="#56AA4E")
    template.main[:] = [app.main]
    template.sidebar[:] = [app.settings_panel]
    logger.info("finishing layout")
    return template


if __name__.startswith("bokeh"):
    view().servable()
