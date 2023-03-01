import pandas as pd
from bokeh.models import (
    ColumnDataSource,
    DataTable,
    HTMLTemplateFormatter,
    NumberFormatter,
    TableColumn,
)

from TP4.modules.base.base_plot import BasePlot
from TP4.utils.formatters import (
    DATA_TABLE_FORMATTER,
    DYA_DATA_TABLE_FORMATTER,
    DYA_DATA_TABLE_FORMATTER_V2,
)


class DataTablePlot(BasePlot):
    """
    Class implementation of the DataTablePlot primitive
    """

    def __init__(self, dict_formats, title, names=None, index_visible=True, height=300, width=1200, **params):
        """
        Constructor of the DataTablePlot
        :param dict_formats: dict
            Associates a formatter type to each column of the table to show,
            Example : {"sales_yag": ["number"], "volume_yag": ["number"], "sales": ["number"],
                          "volume": ["number"]}
        :param title: str
            Plot title
        :param height: int
            plot height
        :param width: int
            plot width
        :param params: inherited args
        """
        super().__init__(**params)
        self.height = height
        self.title = title
        self.width = width
        self.dict_formats = dict_formats
        self.df = pd.DataFrame.from_dict(dict_formats)
        self.formats = self.df.values.tolist()[0]
        self.names = names
        if self.names is None:
            self.names = list(self.dict_formats.keys())
        self.index_visible = index_visible
        self.source = ColumnDataSource(data=dict_formats)
        self.init_columns()

        self.make_figure()
        self.panel = self.get_panel()

    def update_data(self, df):
        """
        At each refresh, update the data of the table to show
        :param df: pandas dataframe
            dataframe to show in the dashboard
        """
        self.df_dict = df.to_dict("list")
        self.source.data = self.df_dict

    def init_columns(self):
        """
        Initialize each columns and their formatter of the table to show
        """
        self.columns = []
        for idx, val in enumerate(self.dict_formats):
            if self.formats[idx] is None:
                self.columns.append(TableColumn(field=val, title=self.names[idx]))
            if self.formats[idx] == "number":
                self.columns.append(
                    TableColumn(
                        field=val,
                        title=self.names[idx],
                        formatter=NumberFormatter(format="0.0", text_align="right"),
                    )
                )
            if self.formats[idx] == "number2":
                self.columns.append(
                    TableColumn(
                        field=val,
                        title=self.names[idx],
                        formatter=NumberFormatter(format="0.00", text_align="right"),
                    )
                )
            if self.formats[idx] == "1000seperator":
                self.columns.append(
                    TableColumn(
                        field=val,
                        title=self.names[idx],
                        formatter=NumberFormatter(format="0,0", text_align="right"),
                    )
                )
            if self.formats[idx] == "pourcentage":
                self.columns.append(
                    TableColumn(
                        field=val,
                        title=self.names[idx],
                        formatter=NumberFormatter(format="0.00%", text_align="center"),
                    )
                )
            if self.formats[idx] == "pourcentage1":
                self.columns.append(
                    TableColumn(
                        field=val,
                        title=self.names[idx],
                        formatter=NumberFormatter(format="0.0%", text_align="center"),
                    )
                )
            if self.formats[idx] == "iya":
                self.columns.append(
                    TableColumn(
                        field=val,
                        title=self.names[idx],
                        formatter=HTMLTemplateFormatter(template=DATA_TABLE_FORMATTER.format(val)),
                    )
                )
            if self.formats[idx] == "dya":
                self.columns.append(
                    TableColumn(
                        field=val,
                        title=self.names[idx],
                        formatter=HTMLTemplateFormatter(template=DYA_DATA_TABLE_FORMATTER.format(val)),
                    )
                )
            if self.formats[idx] == "dya2":
                self.columns.append(
                    TableColumn(
                        field=val,
                        title=self.names[idx],
                        formatter=HTMLTemplateFormatter(template=DYA_DATA_TABLE_FORMATTER_V2.format(val)),
                    )
                )

    def make_figure(self):
        """
        Make the figure using bokeh components and defined parameters
        """
        if self.index_visible:
            self.figure = DataTable(
                source=self.source, columns=self.columns, width=self.width, height=self.height
            )
        else:
            self.figure = DataTable(
                source=self.source, columns=self.columns, width=self.width, height=self.height, index_position=None
            )
