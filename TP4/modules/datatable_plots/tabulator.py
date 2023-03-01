import pandas as pd
import panel as pn
from bokeh.models import HTMLTemplateFormatter, NumberFormatter, StringFormatter

from TP4.modules.base.base_plot import BasePlot
from TP4.utils.formatters import (
    TABULATOR_FORMATTER_CODE,
    TABULATOR_FORMATTER_DYA,
    TABULATOR_FORMATTER_DYA_V2,
    TABULATOR_FORMATTER_IYA,
    TABULATOR_FORMATTER_IYA_V2,
    TABULATOR_FORMATTER_MONITORING,
)


class TabulatorPlot(BasePlot):
    """
    Class implementation of the Tabulator primitive
    """

    def __init__(self, dict_formats, title, names=None, groupby=None, groups=None, pagination=None, page_size=None,
                 frozen_rows=None, frozen_columns=None, hierarchical=None,
                 aggregators=None, editors=None, layout='fit_data_table', header_filters=None, show_index=None,
                 **params):
        """
        Constructor of the Tabulator, official doc from panel https://panel.holoviz.org/reference/widgets/Tabulator.html#formatters

        :param dict_formats: dict
            Associates a formatter type to each column of the table to show,
            Example : {"sales_yag": ["number"], "volume_yag": ["number"], "sales": ["number"],
                          "volume": ["number"]}
        :param title: str
            Plot title
        :param groupby: list
            List of fields to group by on
        :param groups : dict
            for example {'Group 1': ['A', 'B'], 'Group 2': ['C', 'D']}
        :param pagination : str 'remote' or 'local'
        :param page_size : int
            number of max rows per page when using pagination
        :param frozen_rows : list
            List of rows to freeze
        :param frozen_columns : list
            List of columns to freeze
        :param hierarchical : bool
            Whether to render multi-indexes as hierarchical index
        :param aggregators : dict
            A dictionary mapping from index name to an aggregator to be used for hierarchical multi-indexes
        :param titles : dict
            A dictionary mapping from column name to a title to override the name with
        :param layout : str
            Describes the column layout mode with one of the following options 'fit_columns', 'fit_data', 'fit_data_stretch', 'fit_data_fill', 'fit_data_table'.
        :param params: inherited args
        """
        super().__init__(**params)
        self.title = title
        self.dict_formats = dict_formats
        self.groupby = groupby
        self.groups = groups
        self.pagination = pagination
        self.page_size = page_size
        self.frozen_rows = frozen_rows
        self.frozen_columns = frozen_columns
        self.layout = layout
        self.hierarchical = hierarchical
        self.aggregators = aggregators
        self.additional_params = params
        self.editors = self.get_editors(editors)
        self.header_filters = header_filters
        self.show_index = show_index
        if names is None:
            names = [key for key in dict_formats.keys()]
        self.names = {key: names[i] for i, key in enumerate(dict_formats.keys())}
        print(self.names)
        self.parameters_dict = {'groupby': self.groupby,
                                'groups': self.groups,
                                'pagination': self.pagination,
                                'page_size': self.page_size,
                                'frozen_rows': self.frozen_rows,
                                'frozen_columns': self.frozen_columns,
                                'hierarchical': self.hierarchical,
                                'aggregators': self.aggregators,
                                'layout': self.layout,
                                'titles': self.names,
                                'editors': self.editors,
                                'header_filters': self.header_filters,
                                'show_index': self.show_index}

        self.reformat_dict_formats()
        print(self.dict_formats)
        self.df = pd.DataFrame(columns=list(self.dict_formats))
        self.init_formatters()

        self.make_figure()
        self.panel = self.get_panel()

    def reformat_dict_formats(self):
        for col in self.dict_formats:
            if isinstance(self.dict_formats[col], list):
                self.dict_formats[col] = self.dict_formats[col][0]

    def get_editors(self, editors):
        if editors is None:
            editors = {key: {'type': 'editable', 'value': False} for key in self.dict_formats.keys()}
        elif len(editors) < len(self.dict_formats):
            for key, value in self.dict_formats.items():
                if key not in editors.keys():
                    editors[key] = {'type': 'editable', 'value': False}
        print(editors)
        return editors

    def init_formatters(self):
        """
        Initialize each columns and their formatter of the table to show
        """
        self.table_formatters = {}
        for col in self.dict_formats:
            if self.dict_formats[col] == "string":
                self.table_formatters[col] = StringFormatter()
            if self.dict_formats[col] == "number_string":
                self.table_formatters[col] = StringFormatter(text_align="right")
            if self.dict_formats[col] == "number":
                self.table_formatters[col] = NumberFormatter(format="0.0", text_align="right")
            if self.dict_formats[col] == "number2":
                self.table_formatters[col] = NumberFormatter(format="0.00", text_align="right")
            if self.dict_formats[col] == "number2Plus":
                self.table_formatters[col] = NumberFormatter(format="+0.00", text_align="right")
            if self.dict_formats[col] == "1000seperator":
                self.table_formatters[col] = NumberFormatter(format="0,0", text_align="right")
            if self.dict_formats[col] == "1000seperator_round1":
                self.table_formatters[col] = NumberFormatter(format="0,0.0", text_align="right")
            if self.dict_formats[col] == "1000seperatorPlus":
                self.table_formatters[col] = NumberFormatter(format="+0,0", text_align="right")
            if self.dict_formats[col] == "pourcentage":
                self.table_formatters[col] = NumberFormatter(format="0.00%", text_align="center")
            if self.dict_formats[col] == "pourcentage1":
                self.table_formatters[col] = NumberFormatter(format="0.0%", text_align="center")
            if self.dict_formats[col] == "pourcentage1Plus":
                self.table_formatters[col] = NumberFormatter(format="+0.0%", text_align="center")
            if self.dict_formats[col] == "iya":
                self.table_formatters[col] = HTMLTemplateFormatter(template=TABULATOR_FORMATTER_IYA)
            if self.dict_formats[col] == "iya2":
                self.table_formatters[col] = HTMLTemplateFormatter(template=TABULATOR_FORMATTER_IYA_V2)
            if self.dict_formats[col] == "dya":
                self.table_formatters[col] = HTMLTemplateFormatter(template=TABULATOR_FORMATTER_DYA)
            if self.dict_formats[col] == "dya2":
                self.table_formatters[col] = HTMLTemplateFormatter(template=TABULATOR_FORMATTER_DYA_V2)
            if self.dict_formats[col] == "code":
                self.table_formatters[col] = HTMLTemplateFormatter(template=TABULATOR_FORMATTER_CODE)
            if self.dict_formats[col] == "bool":
                self.table_formatters[col] = HTMLTemplateFormatter(template=TABULATOR_FORMATTER_MONITORING)
            if self.dict_formats[col] == "progress_bar":
                self.table_formatters[col] = {'type': 'progress'}
            if self.dict_formats[col] == "tick_cross":
                self.table_formatters[col] = {'type': 'tickCross'}

    def update_data(self, df):
        """
        At each refresh, update the data of the table to show
        :param df: pandas dataframe
            dataframe to plot in the dashboard
        """
        self.figure.value = df

    def make_figure(self):
        """
        Make the figure using panel components and defined parameters
        """
        self.figure = pn.widgets.Tabulator(
            value=self.df, formatters=self.table_formatters, **self.additional_params
        )
        for parameter in list(self.parameters_dict):
            if self.parameters_dict[parameter] is not None:
                self.figure.__setattr__(parameter, self.parameters_dict[parameter])
