import ast
import json
import re
import time
from email import header

import pandas as pd
from google.cloud import bigquery
from logzero import logger

from TP4.constants.constants import (
    ENV,
)
from TP4.modules.base.cpg import CPG
from TP4.utils.api_helper import RequestsApi


class BQBase(object):
    taxonomy = "Global"
    currency = "EUR"
    currency_query = "euro"

    def __init__(self, tenant_id, retrieve_date=True):
        self.tenant_id = tenant_id
        logger.info("getting cpg")
        logger.info("done")
        if retrieve_date:
            self.get_table_properties()
            logger.info("date " + str(self.last_modification) + " has been retrieved")

    def get_currency_query(self):
        if self.currency == "EUR":
            self.currency_query = "euro"
        else:
            self.currency_query = "lc"

    def update_where_with_fields(self, kwargs, unwanted_fields):
        where_condition = """"""
        for key, item in kwargs.items():
            if key not in unwanted_fields:
                if isinstance(item, list):
                    if item != ["ALL"] and len(item) > 0:
                        where_condition += f" AND {key} IN UNNEST({item})"
                elif isinstance(item, str):
                    if item not in ["ALL", "RESET..."] and item is not None:
                        where_condition += f""" AND {key}="{item}" """
                elif isinstance(item, bool):
                    if item:
                        where_condition += f""" AND {key} """
        return where_condition

    def get_where_condition(self, kwargs, unwanted_fields=None):

        if unwanted_fields == None:
            unwanted_fields = []
        kwargs = self.update_time_period_args(kwargs)
        where_condition = self.update_where_with_fields(kwargs, unwanted_fields)
        if "partition" not in unwanted_fields:
            partition_string = self.get_partition(self.taxonomy, self.cpg_company)
            where_condition += partition_string
        return where_condition

    def get_cpg_class(self, prefix=None):
        cpg_class = CPG(self.get_table(prefix=prefix), self.dict_user_attributes)
        return cpg_class

    @staticmethod
    def get_suffix(cpg_company):
        if cpg_company == "CRF":
            return "CRF"
        elif cpg_company == "DEMO":
            return "DEMO"
        else:
            return "CPG"

    def get_user_filters(self, df_user_filters):
        dict_filters = df_user_filters.drop('user', axis=1).to_dict('list')
        user_filters = {}
        is_empty = True

        for key in dict_filters:
            if dict_filters[key][0] is not None and len(dict_filters[key][0]) > 0:
                is_empty = False
                if "[" in dict_filters[key][0] and "]" in dict_filters[key][0]:
                    user_filters[key] = ast.literal_eval(dict_filters[key][0])
                else:
                    user_filters[key] = dict_filters[key]

        return is_empty, user_filters


if __name__ == "__main__":
    BQ = BQBase("101013")
    print(BQ.get_table("ABT_FLAT"))
