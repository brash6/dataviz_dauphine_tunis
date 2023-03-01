import json
from datetime import datetime, timedelta

import pandas as pd
import panel as pn
import param
from panel.io.loading import start_loading_spinner, stop_loading_spinner

from logzero import logger

from TP4.constants.constants import (
    ENV,
    ENV_LOCAL,
    FILTERS_EXPIRY_SECONDS,
    MONTHS,
    TIME_PERIODS,
)
from TP4.modules.base.base_selector import BaseSelectorParent
from TP4.utils.config_spinner import LoadingStyler
from TP4.utils.formatters import currency_mapper, currency_y_axis_formatter
from TP4.utils.gcp import (
    get_dashboard_identifier_from_session,
    get_redis
)
from TP4.utils.notifications import success_notification, warning_notification


class BaseDashboard(param.Parameterized):
    """
    Class implementation of the BaseDashboard
    """

    styler = param.ClassSelector(class_=LoadingStyler)
    selector = param.ClassSelector(class_=BaseSelectorParent)
    loading = param.Boolean(default=False, doc="Whether or not to show the spinner")
    refresh_data = param.Action(label="REFRESH DATA", doc="Refreshes the data")
    save_filters = param.Action(label="SAVE FILTERS", doc="Saves the filters")
    reset_filters = param.Action(label="RESET FILTERS AND RELOAD PAGE", doc="Resets the filters")

    def __init__(self, **params):
        """
        Constructor of the BaseDashboard
        :param params: inherited args
        """
        super().__init__(**params)
        self.first = True
        self.no_data_warning = False
        self.init_currency()

        self.refresh_data = self._refresh_data
        self.save_filters = self._save_filters
        self.reset_filters = self.flush_redis_choice_and_reset_filters

        self.view = pn.Row()

    def init_currency(self):
        self.currency_symbol = '€'
        self.currency_query = 'euro'

    def get_data(self, *_):
        """
        Function to be overrided to get the data using a query
        """
        raise

    def update_plot(self, *_):
        """
        Function to be overrided to update data of the plots declared in the current dashboard
        """
        raise

    def get_settings_panel(self):
        """
        :return: settings of the current dashboard panel
        """
        settings_panel = pn.Column(
            pn.Param(self, parameters=["refresh_data"],
                     widgets={
                         "refresh_data": {"type": pn.widgets.Button(name='REFRESH DATA', button_type="success")}
                     }),
            self.selector.settings_panel,
            pn.Param(self, parameters=["save_filters", "reset_filters"],
                     widgets={
                         "save_filters": {"type": pn.widgets.Button(name='SAVE FILTERS')},
                         "reset_filters": {"type": pn.widgets.Button(name='RESET FILTERS / RELOAD PAGE')},

                     }),
            sizing_mode="stretch_both",
        )

        return settings_panel

    def get_audiences_panel(self):
        """
        :return: settings of the current dashboard panel
        """
        settings_panel = pn.Column(self.audience_import.panel)

        return settings_panel

    def load_layout(self, audience_import=False):
        self.selection_selector = self.get_settings_panel()

        if audience_import:
            self.audiences_selector = self.get_audiences_panel()
            self.settings_panel = pn.Column(self.selection_selector,
                                            pn.layout.Divider(),
                                            self.audiences_selector)
        else:
            self.settings_panel = self.selection_selector

        self.main = pn.Column(*self.panels, sizing_mode="stretch_both")
        logger.info("finished loading the elements")
        self._refresh_data()
        self.view = pn.Row(self.main, self.settings_panel)

    def _save_filters(self, *_):
        filters = self.selector.get_filters()
        filters["global_local"] = self.selector.global_local
        print(f"Here are the filters before save {filters}")
        key = self.get_filter_redis_key()
        string_json = json.dumps(filters)
        r = get_redis()
        r.set(key, string_json, ex=timedelta(FILTERS_EXPIRY_SECONDS))
        success_notification("Filters have been saved")

    def flush_redis_choice_and_reset_filters(self, *_):
        key = self.get_filter_redis_key()
        r = get_redis()
        r.delete(key)
        pn.state.location.reload = True

    def get_email_user(self):
        return get_email_user_from_session()

    def get_filter_redis_key(self):
        project_id = self.cpg_class.project_id
        cpg_company = self.cpg_class.cpg_company
        cpg_country = self.cpg_class.cpg_country
        email = self.get_email_user()
        project_id_supplier_country = f"{email}{project_id}{cpg_company}{cpg_country}"
        print(f"The key is {project_id_supplier_country}")
        return project_id_supplier_country

    def get_user_filters(self):
        key = self.get_filter_redis_key()
        r = get_redis()
        user_filters = r.get(key)
        if user_filters:
            user_filters = json.loads(user_filters)
        print(f"We have gotten the user filters {user_filters}")
        return user_filters

    def set_user_filters(self, filters):
        key = self.get_filter_redis_key()
        string_json = json.dumps(filters)
        r = get_redis()
        r.set(key, string_json, ex=timedelta(FILTERS_EXPIRY_SECONDS))

    def no_data_notification_initialisation(self):
        if self.no_data_warning:
            warning_notification("No data can be retrieved with current selections")

    def get_currency_symbol(self, BQHandler):
        self.cpg_class = BQHandler.get_cpg_class()
        self.currency_symbol, self.currency_code = currency_mapper(self.cpg_class.cpg_country, self.selector.currency)
        self.y_axis_formatter = currency_y_axis_formatter(self.currency_symbol)

    def _refresh_data(self, *_):
        """
        Function to be launched at page initialisation and each time the refresh data button is clicked

        In this order, this function :
            - Get the selected filters
            - Get the data using the get_data() function and the retrieved filters
            - Update the plots by launching the update_plot() function
        """
        print("refreshing")
        self.loading = True

        if self.first:
            user_filters = self.get_user_filters()
            if user_filters:
                print("not_empty --- setting saved user filters")
                self.selector.global_local = user_filters.get("global_local", self.selector.global_local)
                user_filters = self.selector.get_right_filters_from_user_settings(user_filters)
                print(f"The user filters are {user_filters}")
                self.selector.set_filters(user_filters)
                self.filters = self.selector.get_filters()

            else:
                print("is_empty")
                self.filters = self.selector.get_filters()

        else:
            self.filters = self.selector.get_filters()

        print(f"The filters are {self.filters}")
        self.all_valid = True
        self.one_dashboard_error = False

        if self.selector.local_table_exist:
            self.BQHandler.taxonomy = self.selector.global_local
        print(f"The BQHandler taxonomy is {self.selector.global_local}")

        self.BQHandler.currency = self.selector.currency
        self.BQHandler.get_currency_query()
        self.currency_query = self.BQHandler.currency_query
        self.get_currency_symbol(self.BQHandler)

        # timestamp() returns time in nanos
        start_time_in_millis = int(datetime.utcnow().timestamp() * 1000)
        data = self.get_data(self.filters)
        data_load_time = int(datetime.utcnow().timestamp() * 1000) - start_time_in_millis

        do_update = self.show_hide_no_data_warning_pop_up(data, self.one_dashboard_error)
        try:
            if do_update or self.all_valid:
                self.update_plot(data)
        except Exception as e:
            if ENV == ENV_LOCAL:
                raise e
            warning_notification("No data is available for this selection")

        # --------------------------------------------------------------------------
        # IMPORTANT:
        #   This data is consumed by DPS and used in the metrics dashboard usage.
        #   Please contact the IE dev team if you need to change any values.
        # --------------------------------------------------------------------------
        action = "refresh data"
        dashboard_identifier = get_dashboard_identifier_from_session()

        if self.first:
            pn.state.onload(self.no_data_notification_initialisation)

        ############################################
        self.loading = False
        print("end of refresh")

        self.first = False

        return True

    def show_hide_no_data_warning_pop_up(self, data, one_dashboard_error=False):
        do_update = True
        if isinstance(data, dict):
            data = [value for value in data.values()]
        elif not isinstance(data, list):
            data = [data]
        number_valid_df = 0
        for df in data:
            if isinstance(df, pd.DataFrame):
                if df.shape[0] >= 1:
                    number_valid_df += 1
        print(f"The number of valid df is {number_valid_df}")
        if one_dashboard_error:
            if number_valid_df < len(data):
                self.no_data_warning = True
                warning_notification("No data can be retrieved with current selections")
                do_update = False
        else:
            if number_valid_df == 0:
                self.no_data_warning = True
                warning_notification("No data can be retrieved with current selections")
                do_update = False
            print(f'The do_update is {do_update}')

        return do_update

    @param.depends("loading", watch=True)
    def _update_loading_spinner(self):
        """
        Function to start and stop the loading spinner relevantly
        """
        if self.loading:
            start_loading_spinner(self.main)
        else:
            stop_loading_spinner(self.main)

    @param.depends("selector.currency", watch=True)
    def change_currency_and_refresh(self):
        try:
            self._refresh_data()
            success_notification(f"The current currency is now set to {self.currency_symbol}",
                                 duration=2000)
        except:
            pass

    def start_loading(self):
        start_loading_spinner(self.main)

    def stop_loading(self):
        stop_loading_spinner(self.main)


class BaseMeasurementDashboard(param.Parameterized):
    """
    Class implementation of the BaseDashboard
    """

    styler = param.ClassSelector(class_=LoadingStyler)
    loading = param.Boolean(default=False, doc="Whether or not to show the spinner")
    refresh_data = param.Action(label="REFRESH DATA", doc="Refreshes the data")

    def __init__(self, data_init=True, **params):
        """
        Constructor of the BaseDashboard
        :param params: inherited args
        """
        super().__init__(**params)
        self.first = True
        self.no_data_warning = False
        self.data_init = data_init

        self.refresh_data = self._refresh_data

    def get_data(self, *_):
        """
        Function to be overrided to get the data using a query
        """
        raise

    def update_plot(self, *_):
        """
        Function to be overrided to update data of the plots declared in the current dashboard
        """
        raise

    def get_settings_panel(self):
        """

        :return: settings of the current dashboard panel
        """
        css = """
                .bk-root .bk-btn-success {
                    background-image: url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2024%2024%22%20focusable%3D%22false%22%20aria-hidden%3D%22true%22%20fill%3D%22%2373c06b%22%3E%0A%3Cpath%20d%3D%22M17.65%206.35c-1.63-1.63-3.94-2.57-6.48-2.31-3.67.37-6.69%203.35-7.1%207.02C3.52%2015.91%207.27%2020%2012%2020c3.19%200%205.93-1.87%207.21-4.56.32-.67-.16-1.44-.9-1.44-.37%200-.72.2-.88.53-1.13%202.43-3.84%203.97-6.8%203.31-2.22-.49-4.01-2.3-4.48-4.52C5.31%209.44%208.26%206%2012%206c1.66%200%203.14.69%204.22%201.78l-1.51%201.51c-.63.63-.19%201.71.7%201.71H19c.55%200%201-.45%201-1V6.41c0-.89-1.08-1.34-1.71-.71l-.64.65z%22%20%2F%3E%0A%3C%2Fsvg%3E");
                    background-repeat: no-repeat;
                    background-position: 30%;
                    background-size: 25px;
                    color: #73c06b;
                    background-color: white;
                    border: 1px solid #73c06b;
                    font-family: 'Open Sans', sans-serif;
                    font-size: 12px;
                    font-weight: 600;
                    line-height: 1.75;
                    border-radius: 4px;
                    text-indent: +1.5em;
                }

                .bk-root .bk-btn-success:hover {
                    background-color: rgba(115,192,107,0.15);
                }

                .bk-root .bk-btn.bk-btn-success:focus {
                    background-image: url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2024%2024%22%20focusable%3D%22false%22%20aria-hidden%3D%22true%22%20fill%3D%22%2373c06b%22%3E%0A%3Cpath%20d%3D%22M17.65%206.35c-1.63-1.63-3.94-2.57-6.48-2.31-3.67.37-6.69%203.35-7.1%207.02C3.52%2015.91%207.27%2020%2012%2020c3.19%200%205.93-1.87%207.21-4.56.32-.67-.16-1.44-.9-1.44-.37%200-.72.2-.88.53-1.13%202.43-3.84%203.97-6.8%203.31-2.22-.49-4.01-2.3-4.48-4.52C5.31%209.44%208.26%206%2012%206c1.66%200%203.14.69%204.22%201.78l-1.51%201.51c-.63.63-.19%201.71.7%201.71H19c.55%200%201-.45%201-1V6.41c0-.89-1.08-1.34-1.71-.71l-.64.65z%22%20%2F%3E%0A%3C%2Fsvg%3E");
                    background-repeat: no-repeat;
                    background-position: 30%;
                    background-size: 25px;
                }
                """

        pn.config.raw_css.append(css)

        settings_panel = pn.Column(
            pn.Param(self, parameters=["refresh_data"],
                     widgets={
                         "refresh_data": {"type": pn.widgets.Button(name='REFRESH DATA', button_type="success")}
                     }),
            self.selector.settings_panel,
            sizing_mode="stretch_both",
        )
        return settings_panel

    def no_data_notification_initialisation(self):
        if self.no_data_warning:
            warning_notification("No data can be retrieved with current selections")

    def _refresh_data(self, *_):
        """
        Function to be launched at page initialisation and each time the refresh data button is clicked

        In this order, this function :
            - Get the selected filters
            - Get the data using the get_data() function and the retrieved filters
            - Update the plots by launching the update_plot() function
        """
        print("refreshing")
        self.loading = True

        if self.first:
            self.filters = self.selector.get_filters()
        else:
            self.filters = self.selector.get_filters()

        print(f"The filters are {self.filters}")

        """self.BQHandler.currency = self.selector.currency
        self.BQHandler.get_currency_query()
        self.currency_query = self.BQHandler.currency_query"""

        # timestamp() returns time in nanos
        start_time_in_millis = int(datetime.utcnow().timestamp() * 1000)
        data = self.get_data(self.filters)
        data_load_time = int(datetime.utcnow().timestamp() * 1000) - start_time_in_millis

        do_update = self.show_hide_no_data_warning_pop_up(data)
        if do_update:
            # self.get_currency_symbol(self.BQHandler)
            self.update_plot(data)

        # --------------------------------------------------------------------------
        # IMPORTANT:
        #   This data is consumed by DPS and used in the metrics dashboard usage.
        #   Please contact the IE dev team if you need to change any values.
        # --------------------------------------------------------------------------
        action = "refresh data"
        dashboard_identifier = get_dashboard_identifier_from_session()

        if self.first:
            pn.state.onload(self.no_data_notification_initialisation)

        self.loading = False
        print("end of refresh")

        self.first = False

        return True

    def show_hide_no_data_warning_pop_up(self, data):
        do_update = True
        if isinstance(data, dict):
            data = [value for value in data.values()]
        elif not isinstance(data, list):
            data = [data]
        number_valid_df = 0
        for df in data:
            if isinstance(df, pd.DataFrame):
                if df.shape[0] >= 1:
                    number_valid_df += 1
        print(f"The number of valid df is {number_valid_df}")
        if number_valid_df == 0:
            self.no_data_warning = True
            warning_notification("No data can be retrieved with current selections")
            do_update = False
        print(f'The do_update is {do_update}')

        return do_update

    @param.depends("loading", watch=True)
    def _update_loading_spinner(self):
        """
        Function to start and stop the loading spinner relevantly
        """
        if self.loading:
            start_loading_spinner(self.main)
        else:
            stop_loading_spinner(self.main)

    def start_loading(self):
        start_loading_spinner(self.main)

    def stop_loading(self):
        stop_loading_spinner(self.main)


class BaseExampleDashboard(BaseMeasurementDashboard):

    def __init__(self, **params):
        super().__init__(**params)
