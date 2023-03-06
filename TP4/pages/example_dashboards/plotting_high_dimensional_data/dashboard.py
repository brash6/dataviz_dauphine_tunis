import holoviews as hv
import panel as pn
import param
import pandas as pd
import umap
from bokeh.models import BoxSelectTool, BoxZoomTool, ResetTool, TapTool, SaveTool, PanTool, WheelZoomTool
from sklearn import decomposition, manifold
from sklearn.preprocessing import MinMaxScaler

from TP4.constants.constants import LR_SINGULAR_COLOR, LR_DIVERGING_COLORS_LONG, RED, GREEN
from TP4.modules.barplots.simple_barplot import SimpleBarPlot
from TP4.modules.base.base_dashboard import BaseExampleDashboard
from TP4.modules.datatable import DataTablePlot
from TP4.modules.panel_text import PanelText
from TP4.modules.heatmaps.heatmap import Heatmap
from TP4.modules.scatterplots.basic_scatterplot import BasicScatterPlot
from TP4.pages.example_dashboards.plotting_high_dimensional_data.figures import BoxPlot
from TP4.pages.example_dashboards.plotting_high_dimensional_data.queries import BQClient
from TP4.pages.example_dashboards.plotting_high_dimensional_data.selector import (
    VGSelector,
)
from TP4.utils.view import get_template
from TP4.awesome_panel_extensions.site import site

hv.extension("bokeh")

APPLICATION = site.create_application(
    url="plotting_high_dimensional_data",
    name="Plotting High Dimensional Data",
    tags=["UX"],
    folder="example_dashboards"
)


class Dashboard(BaseExampleDashboard):
    # Declare here the used selector
    selector = param.ClassSelector(class_=VGSelector)
    switch_button = param.ObjectSelector(default='PCA')
    n_neighbors = param.Integer(30)
    min_distance = param.Number(0.1)

    # Doesn't change, used to instantiate all the plots to render using Panel
    panels = param.List()

    def __init__(self, BQHandler: BQClient, **params):
        super().__init__(**params)
        self.BQHandler = BQHandler

        # Create a selector
        self.selector = VGSelector(self.BQHandler)

        df_data = pd.read_csv("TP4/pages/example_dashboards/new_beverage_chemistry.csv")
        df_data = df_data.drop("Id", axis=1)

        self.switch_button_panel = pn.Param(
            self,
            name="",
            parameters=["switch_button"],
            widgets={"switch_button": pn.widgets.RadioButtonGroup(name='switch_button', value='PCA',
                                                                         options=['PCA', 'T-SNE', 'UMAP'],
                                                                         width=300, align='center')})

        self.n_neighbors_panel = pn.Param(self,
                                               name="",
                                               parameters=["n_neighbors"],
                                               widgets={
                                                   "n_neighbors": pn.widgets.IntSlider(start=5, end=50, value=30,
                                                                                            step=1,
                                                                                            name="Number of Neighbors",
                                                                                            max_width=310,
                                                                                            align='center')})

        self.min_distance_panel = pn.Param(self,
                                          name="",
                                          parameters=["min_distance"],
                                          widgets={
                                              "min_distance": pn.widgets.FloatSlider(start=0, end=1, value=0.1,
                                                                                  name="Min distance",
                                                                                  max_width=310,
                                                                                  align='center')})

        # Create Plots
        self.plot_text = PanelText(text="""
        An example of dashboard for exploring and plotting high dimensional data
        """, about=True)

        self.data_table = DataTablePlot(
            dict_formats={
                "fixed acidity": ["number"],
                "volatile acidity": ["number"],
                "citric acid": ["number"],
                "residual sugar": ["number"],
                "chlorides": ["number"],
                "free sulfur dioxide": ["number"],
                "total sulfur dioxide": ["number"],
                "density": ["number"],
                "pH": ["number"],
                "sulphates": ["number"],
                "alcohol": ["number"],
                "quality": ["number"],
            },
            title="New beverage chemistry and quality dataset overview",
        )

        self.heatmap_correlation = Heatmap(
            title="Correlation Matrix",
            tools=[SaveTool()],
            kpi='Feature 1',
            x='Feature 2',
            y='platform',
        )

        # Simple BarPlot
        self.quality_grades_distribution = SimpleBarPlot(
            x_axis_label="Quality Score",
            y_axis_label="Frequency",
            title="Quality Scores distribution",
            colors=LR_SINGULAR_COLOR,
            tools=[BoxSelectTool(), ResetTool(), TapTool()],
            tooltips="""
                             <b>Quality Score : </b> @x <br>
                             <b>Frequency : </b> @y
                             """,
        )

        boxplot_data = self.preprocess_for_boxplot(df_data.drop(["quality"], axis=1))
        self.boxplot = BoxPlot(
            boxplot_data,
            x_axis_label="Feature",
            y_axis_label="Normalized value",
            title="Features distribution",
        )

        self.projection_scatter_plot = BasicScatterPlot(title="Projection of beverages in 2 dimensions",
                                                              x_axis_label="",
                                                              y_axis_label="",
                                                              tools=[SaveTool(), PanTool(), WheelZoomTool()],
                                                              tooltips="""
                                                                          <b>quality: </b> @labels
                                                                          """, )

        # Add in the panels list all the declared plot figures
        self.panels = [
            self.plot_text.panel,
            self.data_table.panel,
            self.heatmap_correlation.panel,
            self.boxplot.panel,
            self.quality_grades_distribution.panel,
            pn.Row(pn.Column(self.switch_button_panel, margin=(0, 10, 0, 10)),
                   pn.Column('', max_width=100)),
            pn.Row(self.n_neighbors_panel, self.min_distance_panel),
            self.projection_scatter_plot.panel,
        ]

        self.n_neighbors_panel.widgets["n_neighbors"].visible = False
        self.min_distance_panel.widgets["min_distance"].visible = False

        # Doesn't change
        self.settings_panel = self.get_settings_panel()
        self.main = pn.Column(*self.panels, sizing_mode="stretch_both")

        self.view = pn.Row(self.main, self.settings_panel)

    @param.depends("switch_button", watch=True, on_init=False)
    def launch_dimension_reduction(self):
        if not self.first:
            print("test")
            if self.switch_button == "UMAP" and self.n_neighbors_panel.widgets["n_neighbors"].visible == False:
                self.n_neighbors_panel.widgets["n_neighbors"].visible = True
                self.min_distance_panel.widgets["min_distance"].visible = True
            elif self.switch_button != "UMAP":
                self.n_neighbors_panel.widgets["n_neighbors"].visible = False
                self.min_distance_panel.widgets["min_distance"].visible = False
                self.loading = True
                self.update_plot(self.loaded_data)
                self.loading = False
            else:
                self.loading = True
                self.update_plot(self.loaded_data)
                self.loading = False

    def normalize_data(self, df):
        scaler = MinMaxScaler()
        df_norm = scaler.fit_transform(df)
        df_norm = pd.DataFrame(df_norm)
        df_norm.columns = df.columns.values
        return df_norm

    def preprocess_for_boxplot(self, data):
        data = self.normalize_data(data)
        df = pd.DataFrame()
        for col in list(data.columns.values):
            df_col = pd.DataFrame(data[col])
            df_col["kind"] = col
            df_col = df_col.rename(columns={col: "hwy"})
            cols = ["kind", "hwy"]
            df_col = df_col[cols]
            df = df.append(df_col, ignore_index=True)
        return df

    def reduce_dimension(self, data):
        if self.switch_button == "PCA":
            results = self.launch_PCA(data)
        elif self.switch_button == "T-SNE":
            results = self.launch_TSNE(data)
        else:
            results = self.launch_UMAP(data)
        return results

    def launch_PCA(self, data):
        pca = decomposition.PCA(n_components=2)
        X_pca = pca.fit_transform(data)
        results = pd.DataFrame(X_pca, columns=[["0", "1"]])
        results["quality"] = data["quality"]
        return results

    def launch_TSNE(self, data):
        tsne = manifold.TSNE(n_components=2, init='random', random_state=42, perplexity=30)
        X_tsne = tsne.fit_transform(data)
        results = pd.DataFrame(X_tsne, columns=[["0", "1"]])
        results["quality"] = data["quality"]
        return results

    def launch_UMAP(self, data):
        um = umap.UMAP(n_neighbors=self.n_neighbors, min_dist=self.min_distance, metric="euclidean")
        X_umap = um.fit_transform(data)
        results = pd.DataFrame(X_umap, columns=[["0", "1"]])
        results["quality"] = data["quality"]
        return results

    def get_data(self):
        print("getting data")

        df_data = pd.read_csv("TP4/pages/example_dashboards/new_beverage_chemistry.csv")
        df_data = df_data.drop("Id", axis=1)

        self.loaded_data = df_data

        return df_data

    def update_plot(self, data):
        print("update")

        self.data_table.update_data(df=data)
        self.heatmap_correlation.update_heatmap_correlation(data)

        quality_distrib = pd.DataFrame(data.quality.value_counts().reset_index()).sort_values(by=['index'])
        print(quality_distrib)
        self.quality_grades_distribution.figure.x_range.factors = list(quality_distrib["index"].astype(str))
        self.quality_grades_distribution.source.data = dict(
            x=list(quality_distrib["index"].astype(str)),
            y=list(quality_distrib["quality"].astype(str)),
        )

        projection_results = self.reduce_dimension(data)
        qualities = self.get_flat_list(projection_results, "quality")
        qualities_strings = [str(x) for x in qualities]

        first_axis = self.get_flat_list(projection_results, "0")
        second_axis = self.get_flat_list(projection_results, "1")

        color_list = self.create_color_list(qualities)

        self.projection_scatter_plot.source.data = dict(
            labels=qualities_strings,
            x=first_axis,
            y=second_axis,
            size=[20] * len(qualities),
            color=color_list,
        )

    def create_color_list(self, elements):
        color_list = []
        for elem in elements:
            if elem < 7:
                color_list.append(RED)
            else:
                color_list.append(GREEN)
        return color_list

    def get_flat_list(self, data, col):
        res = data[col].values.tolist()
        flat_res = [item for sublist in res for item in sublist]
        return flat_res

    def get_user_filters(self):
        return False

    def _refresh_data(self, *_):
        self.loading = True
        self.first = False
        data = self.get_data()
        self.update_plot(data)
        self.loading = False

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
    return get_template(BQClient, Dashboard, name_tab="Plotting high dimensional data")


if __name__.startswith("bokeh"):
    view().servable()
