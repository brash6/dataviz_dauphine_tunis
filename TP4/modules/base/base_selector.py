import datetime
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import panel as pn
import param
from bokeh.models import ColumnDataSource
from panel.io.loading import start_loading_spinner, stop_loading_spinner

from TP4.modules.base.cpg import CPG
from TP4.modules.panel_text import PanelText
from TP4.utils.config_spinner import LoadingStyler
from TP4.utils.notifications import error_notification


class BaseSelectorParent(param.Parameterized):
    def __init__(self, **params):
        super().__init__(**params)


class BaseSelector(BaseSelectorParent):
    """
    Class implementation of a Base Selector
    """

    settings_panel = param.Parameter(doc="A panel containing the settings of the LoadingStyler")

    cpg_table = param.String()
    cpg_country = param.String()

    panels = param.List()
    loading = param.Boolean(default=False, doc="""Whether or not to show the loading indicator""")

    text = """
        ### Warning

        <hr>

        You have to select values in all fields
        """
    warning_pop_up_reset = pn.pane.Alert(text, alert_type="danger", visible=False)

    view = param.Parameter()

    def __init__(self, **params):
        """
        Constructor of the BaseSelector class
        :param params: args
        """
        super().__init__(**params)

    @param.depends("loading", watch=True)
    def _update_loading_spinner(self):
        """
        Launch loading spinner at each data refresh
        :return:
        """
        if self.loading:
            self._start_loading_spinner()
        else:
            self._stop_loading_spinner()

    def _start_loading_spinner(self, *_):
        """
        Start loading spinner
        :param _: args
        """
        for panel in [self.settings_panel]:
            start_loading_spinner(panel)

    def _stop_loading_spinner(self, *_):
        """
        Stops the loading spinner
        :param _: args
        """
        for panel in [self.settings_panel]:
            stop_loading_spinner(panel)


class BaseSelectorMsmt(BaseSelector):
    def set_study_id(self, df):
        try:
            if "study" in pn.state.session_args.keys():
                study = str(pn.state.session_args["study"][0].decode("utf-8"))
                if study in list(df["study_uid"].unique()):
                    self.param.study_uid.default = study
                else:
                    raise Exception
            else:
                self.param.study_uid.default = list(df["study_uid"].unique())[0]
        except Exception as e:
            pn.state.onload(self.display_error_no_study)
            self.param.study_uid.default = list(df["study_uid"].unique())[0]

    def display_error_no_study(self):
        error_notification("""The study is not available for this dashboard, the dashboard has been loaded with another study
                           """)

    def get_df_from_study(self, df):
        df = df[df["study_uid"] == self.study_uid]
        return df

    def get_word_or_first_object_in_list(self, list_to_check, word):
        if word in list_to_check:
            return word
        else:
            return list_to_check[0]

    def get_total_or_first_object(self, list_to_check):
        return self.get_word_or_first_object_in_list(list_to_check, "total")

    def get_all_or_first_object(self, list_to_check):
        return self.get_word_or_first_object_in_list(list_to_check, "all")


class BaseDynamicSelector(BaseSelector):
    reset_button = param.Action(lambda x: x.param.trigger("reset_button"), label="Reset Fields")
    global_local = param.Selector(["Global", "Local"], default="Local")
    currency = param.Selector(["EUR", "Local Currency"], default="EUR")
    time_period_type = param.Selector()
    is_active_store = param.Selector(["ALL Stores", "Active 24M only"], default="ALL Stores")
    time_period = param.ObjectSelector()

    country = param.ObjectSelector()
    supplier = param.ObjectSelector()
    global_channel = param.ObjectSelector()
    specific_channel = param.ObjectSelector()
    store = param.ObjectSelector()
    sector = param.ObjectSelector()
    department = param.ObjectSelector()
    classes = param.ObjectSelector()
    category = param.ObjectSelector()
    sub_category = param.ObjectSelector()
    brand = param.ObjectSelector()
    unit_need = param.ObjectSelector()
    item = param.ObjectSelector()
    barcode = param.ObjectSelector()

    list_time_field = ["time_period_type", "time_period"]
    list_channel_field = ["supplier", "global_channel", "specific_channel", "sector", "department", "store", "classes"]
    list_taxonomy_field = ["supplier", "classes", "category", "sub_category", "brand", "unit_need", "item", "barcode"]
    list_taxonomy_channel_field = ["supplier", "global_channel", "specific_channel", "sector", "department",
                                   "classes", "category", "sub_category", "brand", "unit_need"]
    list_intersect_channel_taxo = ["supplier", "global_channel", "specific_channel", "classes"]

    def __init__(self, cpg_class: CPG = None, selection_fields=None, global_local_currency=True, **params):
        super().__init__(**params)
        self.set_attributes_from_cpg_class(cpg_class)
        print(f"The CPG_COMPANY is {self.cpg_company}")
        self.check_if_local_is_available()

        self.global_local_currency = global_local_currency

        ### change AB
        self.time_selection_fields = {key: value for key, value in selection_fields.items() if "time" in key}
        self.selection_fields = self.format_selection_field(selection_fields)

        # Temporary disablement of local global local taxonomy for italy
        if self.cpg_country == "ITA":
            with param.discard_events(self):
                self.global_local = "Global"

    def set_attributes_from_cpg_class(self, cpg_class):
        self.tenant_id = cpg_class.tenant_id
        self.cpg_tenant_project_id = cpg_class.cpg_tenant_project_id
        self.project_id = cpg_class.project_id
        self.cpg_company = cpg_class.cpg_company
        self.cpg_country = cpg_class.cpg_country
        self.supplier_cpg = cpg_class.supplier_cpg
        self.global_partitions = cpg_class.global_partitions
        self.local_partitions = cpg_class.local_partitions
        self.country_partition = cpg_class.country_partition
        self.cpg_table = cpg_class.cpg_table
        self.is_custom_taxonomy = cpg_class.is_custom_taxonomy

    def format_selection_field(self, selection_field):
        selection_field = self.remove_class_from_dict(selection_field)

        for key, value in selection_field.items():
            if isinstance(value, str):
                selection_field[key] = {"type": value}
        if "time_period_type" in selection_field.keys():
            if "type" not in selection_field["time_period_type"].keys():
                selection_field["time_period_type"]["type"] = "mono"
            if "time_period" in selection_field.keys():
                if "type" not in selection_field["time_period"].keys():
                    selection_field["time_period"]["type"] = "multi"
        elif "time_period" in selection_field.keys():
            if "type" not in selection_field["time_period"].keys():
                selection_field["time_period"]["type"] = "mono"

        print(f"The selection field is {selection_field}")
        return selection_field

    def remove_class_from_dict(self, selection_field):
        new_selection_field = {}
        for k, v in selection_field.items():
            if k == "class":
                new_selection_field["classes"] = v
            else:
                new_selection_field[k] = v
        return new_selection_field

    @param.depends("global_local", watch=True)
    def change_taxo(self):
        self.loading = True
        if self.local_table_exist:
            self.get_all_dataframes()
            self.init_fields_settings_panel()
        self.loading = False

    @param.depends("time_period_type", watch=True)
    def update_time_period(self):
        """
        Update the time periods fields depending on the selected time period type
        """
        if "time_period_type" in self.selection_fields.keys():
            df_time_period = self.time_period_fields[self.time_period_fields.time_period_type == self.time_period_type]
            list_object = list(df_time_period["time_period"].unique())
            if self.time_period_type == "MONTH":
                list_object = self.reorder_date_list(list_object)
            elif self.time_period_type == "PERIOD":
                list_object = self.reorder_period_list(list_object)
            self.param.time_period.objects = list_object
            if self.time_period in list_object:
                default = self.time_period
            else:
                default = list_object[0]
            if self.get_type_selection("time_period") == "mono":
                self.param.set_param("time_period", default)
            elif self.get_type_selection("time_period") == "multi":
                if self.time_period not in list_object:
                    self.time_period = []

    def add_time_period(self):
        for key, value in self.time_selection_fields.items():
            if key == "time_period_type":
                time_period_type_objects = list(self.time_period_fields["time_period_type"].unique())
                print(time_period_type_objects)
                default_time_period_type = time_period_type_objects[0]
                if isinstance(value, dict):
                    if "values" in value.keys():
                        time_period_type_objects = value["values"]
                        default_time_period_type = time_period_type_objects[0]
                    if "default" in value.keys():
                        default_time_period_type = value["default"]
                if {"WEEK", "MONTH", "PERIOD", "QUARTER", "SEMESTER"} == set(time_period_type_objects):
                    time_period_type_objects = {"WK": "WEEK", "MTH": "MONTH", "PER": "PERIOD", "QTR": "QUARTER",
                                                "SEM": "SEMESTER"}
                    self._add_parameter('time_period_type',
                                        param.Selector(default=default_time_period_type,
                                                       objects=time_period_type_objects))
                else:
                    self._add_parameter('time_period_type',
                                        param.Selector(default=default_time_period_type,
                                                       objects=time_period_type_objects))

            elif key == "time_period":
                if isinstance(value, dict):
                    if "objects" in value.keys():
                        list_objects = value["objects"]
                    else:
                        list_objects = list(self.time_period_fields.time_period.unique())
                    if "default" in value.keys():
                        default = value["default"]
                    else:
                        default = list_objects[0]
                    self._add_parameter("time_period", param.Selector(default=default, objects=list_objects))
                else:
                    list_objects = list(self.time_period_fields.time_period.unique())
                    list_objects = self.reorder_date_list(list_objects)
                    if self.get_type_selection(key) == "mono":
                        self._add_parameter(key, param.ObjectSelector())
                    elif self.get_type_selection(key) == "multi":
                        self._add_parameter(key, param.ListSelector())
                    print(f"The object list is {list_objects}")
                    self.param.time_period.objects = list_objects

    def get_time_period_dataframe(self):
        time_period_keys = list(self.time_selection_fields.keys())
        self.time_period_fields = self.get_distinct_fields(time_period_keys, self.cpg_table,
                                                           global_local=self.global_local)

    def get_distinct_fields(self, keys, cpg_table, global_local="Global"):
        if len(keys) == 0:
            return None
        if global_local == "Local" and self.local_table_exist:
            cpg_table = cpg_table + "_LOCAL"
            partition_string = self.get_partition(use_local=True, cpg_company=self.cpg_company)
        else:
            partition_string = self.get_partition(use_local=False, cpg_company=self.cpg_company)

        for index in range(len(keys)):
            if keys[index] == "classes":
                keys[index] = "class"
        select_fields_query = ",".join(keys)
        str_where = ""
        if self.cpg_country != "INTER":
            str_where = f"WHERE country='{self.cpg_country}'"
        query = f"""
                SELECT DISTINCT {select_fields_query}
                FROM {cpg_table}
                {str_where} {partition_string}
                """

        if self.tenant_id is None:
            tenant_id = get_tenant_id_from_session()
        else:
            tenant_id = self.tenant_id

        # labels have to be str:str or BigQuery complains
        labels = {"tenant_id": str(tenant_id)}
        fields = read_gbq_gcp(query, labels=labels)
        fields = fields.dropna()
        return fields

    def init_fields_settings_panel(self):
        self.get_default_values()
        self.set_selector_fields()
        self.list_selector_fields = self.get_list_selector_fields()
        self.widget_selector_fields = self.get_widget_selector_fields()

        self.init_data()

        self.update_time_period()
        # for function_to_launch in [self.update_supplier,]:
        # self.update_class, self.update_category, self.update_sub_categ,
        #                            self.update_brand, self.update_item]:
        #     function_to_launch()
        self.current_filters = self.get_filters()

    def run_multithread(self, list_functions):
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(f) for f in list_functions]
            for idx, future in enumerate(as_completed(futures)):
                index = future.result()

    def get_type_selection(self, key):
        return self.selection_fields[key]["type"]

    def get_mono_and_multi_fields(self):
        mono = []
        multi = []
        for key in self.selection_fields:
            if key in ['time_period_type', 'time_period']:  ##AB
                pass
            elif self.get_type_selection(key) == "multi":
                multi.append(key)
            elif self.get_type_selection(key) == "mono":
                mono.append(key)

        return mono, multi

    def get_default_supplier(self):
        self.default_supplier = self.supplier_cpg
        # TODO: To be addressed
        """if self.cpg_company == "CRF":
            self.default_supplier"""
        print(f"The default supplier is {self.default_supplier}")

    def set_selector_fields(self):
        for key in self.multi:
            if key == "supplier":
                self._add_parameter(key, param.ListSelector(
                ))
            elif key == "country":
                self._add_parameter(key, param.ListSelector())
            else:
                self._add_parameter(key, param.ListSelector())
        for key in self.mono:
            self._add_parameter(key, param.ObjectSelector())

    def get_filters(self):
        filters = {}
        for key, value in self.selection_fields.items():
            filter_value = getattr(self, key)
            if key == 'is_active_store':
                if "ALL" in filter_value:
                    filters[key] = False
                else:
                    filters[key] = True
            else:
                filters[key] = filter_value

        return filters

    def get_list_selector_fields(self):
        list_selector_fields = []
        for key, value in self.selection_fields.items():
            if "is_active_store" not in key:
                list_selector_fields.append(key)
        if self.only_mono:
            list_selector_fields.insert(0, "reset_button")

        return list_selector_fields

    def update_filters(self, df, filters):
        right_filters = {}
        for key, value in filters.items():
            if key in self.selection_fields.keys():
                if key in df.columns:
                    param_selector_element = getattr(self.param, key)
                    if isinstance(value, list):
                        if len(value) > 0:
                            new_value = []
                            for i in value:
                                if i in df[key].unique():
                                    new_value.append(i)
                            df = df[df[key].isin(new_value)]
                            if self.get_type_selection(key) == "multi":
                                right_filters[key] = new_value
                            elif self.get_type_selection(key) == "mono":
                                if len(new_value) > 0:
                                    right_filters[key] = new_value[0]
                                else:
                                    right_filters[key] = param_selector_element.objects[0]
                                df = df[df[key] == right_filters[key]]
                        elif len(value) == 0:
                            if self.get_type_selection(key) == "multi":
                                dict_key = self.selection_fields[key]
                                if "default" not in dict_key.keys() or dict_key["default"] == False:
                                    right_filters[key] = value

                    elif isinstance(value, str):
                        if value in df[key].unique():
                            if self.get_type_selection(key) == "multi":
                                right_filters[key] = [value]
                                df = df[df[key] == value]
                            elif self.get_type_selection(key) == "mono":
                                right_filters[key] = value
                                df = df[df[key] == right_filters[key]]

        for key, value in self.selection_fields.items():
            if "time" not in key and "country" != key:
                if key in df.columns:
                    if key not in right_filters.keys() and self.get_type_selection(key) == "mono":
                        right_filters[key] = list(df[key].unique())[0]
                        df = df[df[key] == right_filters[key]]
                        return self.update_filters(df, right_filters)

        return right_filters

    def set_filters(self, filters):
        for key, value in filters.items():
            print(f"The key is {key}")
            print(f"The value is {value}")
            self.param.set_param(key, value)

    def add_button_time_period(self):
        time_widget_selector = {}
        for key, value in self.time_selection_fields.items():
            if key == "time_period_type":
                time_widget_selector[key] = {"type": pn.widgets.RadioButtonGroup, "sizing_mode": "fixed"}
            elif key == "time_period":
                if self.get_type_selection(key) == "multi":
                    button_type = pn.widgets.MultiChoice
                elif self.get_type_selection(key) == "mono":
                    button_type = pn.widgets.Select
                elif isinstance(value, dict):
                    button_type = pn.widgets.RadioButtonGroup
                time_widget_selector[key] = {"type": button_type, "sizing_mode": "fixed"}
        return time_widget_selector

    def get_widget_selector_fields(self):
        widget_selector_fields = {}

        if self.only_mono:
            widget_selector_fields["reset_button"] = {"type": pn.widgets.Button, "sizing_mode": "fixed"}

        widget_time_period = self.add_button_time_period()
        widget_selector_fields.update(widget_time_period)

        for key, value in self.selection_fields.items():
            if "time" not in key and "active" not in key:
                if self.get_type_selection(key) == "multi":
                    button_type = pn.widgets.MultiChoice
                elif self.get_type_selection(key) == "mono":
                    button_type = pn.widgets.Select
                if key == "global_channel":
                    widget_selector_fields[key] = {"type": button_type, "name": "Store / E-Commerce",
                                                   "sizing_mode": "fixed"}
                elif key == "specific_channel":
                    widget_selector_fields[key] = {"type": button_type, "name": "Channel", "sizing_mode": "fixed"}
                elif key == "classes":
                    widget_selector_fields[key] = {"type": button_type, "name": "Class", "sizing_mode": "fixed"}
                elif key == "department":
                    widget_selector_fields[key] = {"type": button_type, "name": "Sub-sector", "sizing_mode": "fixed"}
                else:
                    widget_selector_fields[key] = {"type": button_type, "sizing_mode": "fixed"}

        return widget_selector_fields

    def get_partition(self, use_local, cpg_company):
        if int(self.tenant_id) == 101016:
            partition_string = ""
        elif cpg_company == "CRF":
            partition_column = "country_partition"
            partition_string = f" AND {partition_column}={self.country_partition}"
        elif cpg_company == "DEMO":
            partition_string = ""
        else:
            partition_column = "sub_category_id"
            if use_local:
                partitions = self.local_partitions
            else:
                partitions = self.global_partitions
            # partition_string = f""
            partition_string = f" AND {partition_column} IN UNNEST({partitions})"

        return partition_string

    def get_selector_fields(self, cpg_table):
        list_keys_query = [i for i in self.selection_fields.keys() if i not in ["time_period_type", "time_period"]]
        fields = self.get_distinct_fields(list_keys_query, cpg_table, self.global_local)
        return fields

    @param.depends("reset_button", watch=True)
    def reset_fields(self):
        self.set_manually = []
        self.init_fields_settings_panel()

    def get_dif_filters(self, new_filters):
        changed_filters = []
        for k in new_filters:
            if new_filters[k] != self.current_filters[k]:
                changed_filters.append(k)
        return changed_filters

    def format_filter(self, filter):
        if isinstance(filter, str):
            filter = [filter]
        elif filter is None:
            filter = []
        return filter

    def check_if_item_in_selection_fields(self, item):
        if item in self.selection_fields.keys():
            return True
        else:
            return False

    def filter_df_with_dict(self, df, dict_filters):
        for key, filter in dict_filters.items():
            print(f"Filtering for {key}, {filter}")
            filter = self.format_filter(filter)
            if len(filter) > 0:
                df = df[df[key].isin(filter)]
        return df

    def update_field(self, list_field_to_update, list_field_parent):
        if not self.check_if_item_in_selection_fields(list_field_parent[-1]):
            return True
        filters = self.get_filters()
        parent_field_list = [i for i in list_field_parent if i not in list_field_to_update]
        dict_relevant_filters = {key: filters[key] for key in parent_field_list if key in filters.keys()}

        df = self.get_df_from_field(list_field_parent[-1])
        print("----- DF FROM FIELD ------")
        print(df)
        df = self.filter_df_with_dict(df, dict_relevant_filters)
        print("----- DF ------")
        print(df)
        for field_to_update in list_field_to_update:
            if self.check_if_item_in_selection_fields(field_to_update):
                try:
                    list_objects = list(df[field_to_update].sort_values().unique())
                    param_selector_element = getattr(self.param, field_to_update)
                    param_selector_element.objects = list_objects
                    if self.get_type_selection(field_to_update) == "mono":
                        cur_value = getattr(self, field_to_update)
                        if cur_value not in list_objects:
                            cur_value = list_objects[0]

                        self.param.set_param(field_to_update, cur_value)
                        df = df[df[field_to_update] == cur_value]
                    elif self.get_type_selection(field_to_update) == "multi":
                        if getattr(self, field_to_update) not in list_objects:
                            self.param.set_param(field_to_update, [])
                except:
                    list_objects = list(df[field_to_update].sort_values().unique())
                    param_selector_element = getattr(self.param, field_to_update)
                    param_selector_element.objects = list_objects

    @param.depends("is_active_store", watch=True, on_init=False)
    def update_with_active_store(self):
        if "store" in self.selection_fields.keys():
            df = self.get_df_from_field("store")
            if "ALL" in self.is_active_store:
                self.param.store.objects = list(df["store"].unique())
            else:
                self.param.store.objects = list(df[df["is_active_store"] == True]["store"].unique())

    @staticmethod
    def num_sort(test_string):
        return list(map(int, re.findall(r'\d+', test_string)))[0]

    def reorder_period_list(self, list_periods):
        cytd = False
        if "CYTD" in list_periods:
            cytd = True
        list_periods = [i for i in list_periods if i != "CYTD"]
        print(list_periods)
        list_periods.sort(key=self.num_sort)
        if cytd:
            list_periods.append("CYTD")
        return list_periods

    def reorder_date_list(self, list_objects):
        if "202" in list_objects[0]:
            try:
                good_list = sorted(list_objects, key=lambda m: datetime.datetime.strptime(m, "%B %Y"))
            except:
                good_list = list_objects
        else:
            try:
                good_list = sorted(list_objects, key=lambda m: datetime.datetime.strptime(m, "%B"))
            except:
                good_list = list_objects
        for i in range(0, len(good_list)):
            good_list[i] = f"{i + 1} - {good_list[i]}"
        return good_list

    def get_master_category(self):
        master_category = None
        for key in ["supplier", "classes", "category", "sub_category"]:
            if key in self.selection_fields.keys():
                if self.selection_fields[key].get("default", True):
                    master_category = key
                    print(f"The master category is {master_category}")
                break
        return master_category

    def set_key_and_update_df(self, key, df):
        if key in self.default_values.keys():
            try:
                list_unique = list(df[key].sort_values().unique())
                default_value = self.default_values[key]
                default_value = [i for i in list_unique if default_value == i][0]
            except:
                default_value = self.default_values[key]
        else:
            default_value = list(df[key].sort_values().unique())[0]
        param_selector_element = getattr(self.param, key)
        param_selector_element.objects = list(df[key].sort_values().unique())
        if default_value == False:
            return df
        df = df[df[key] == default_value]
        if self.get_type_selection(key) == "multi":
            default_value = [default_value]
        print(f"Setting the param to {default_value} for param {key}")
        self.param.set_param(key, default_value)
        return df

    def get_master_keys(self, master_category):
        list_master_keys = ["country", "global_channel", "specific_channel"]
        if master_category is not None:
            list_master_keys.append(master_category)
            print(f"The list of master keys is {list_master_keys}")
        return list_master_keys

    def build_distinct_fields(self, list_fields, df):
        """
        Initialize the possible fields for each filter

        :param df: pandas dataframe
            dataframe containing the possible fields for each filter
        """
        master_category = self.get_master_category()
        master_keys_global = self.get_master_keys(master_category)
        master_keys = [i for i in self.selection_fields.keys() if i in master_keys_global]

        self.current_filters = self.get_filters()
        for key in master_keys:
            if key in list_fields:
                df = self.set_key_and_update_df(key, df)
        for key in list_fields:
            if key in self.selection_fields.keys():
                value = self.selection_fields[key]
                if key not in master_keys and "time" not in key:
                    if key == "time_period" and self.get_type_selection(key) == "mono":
                        self.set_key_and_update_df(key, self.time_period_fields[
                            self.time_period_fields.time_period_type == self.time_period_type])
                    else:
                        if self.get_type_selection(key) == "mono":
                            df = self.set_key_and_update_df(key, df)
                        elif self.has_default_selection(key):
                            df = self.set_key_and_update_df(key, df)
                        else:
                            param_selector_element = getattr(self.param, key)
                            self.param.set_param(key, [])
                            param_selector_element.objects = list(df[key].unique())

        self.current_filters = self.get_filters()

    def has_default_selection(self, key):
        dict_key = self.selection_fields[key]
        if "default" in dict_key.keys() and dict_key["default"] == True:
            return True
        else:
            return False

    def get_default_selection(self, field, list_choices, str_to_match):
        dict_select_field = self.selection_fields[field]
        if "default" in dict_select_field:
            default_value = dict_select_field["default"]
            if default_value in list_choices:
                self.default_values[field] = default_value
            elif default_value == False:
                self.default_values[field] = False
            else:
                self.default_values[field] = [i for i in list_choices if str_to_match in i.lower()][0]
        else:
            self.default_values[field] = [i for i in list_choices if str_to_match in i.lower()][0]

    def init_data(self):
        raise
