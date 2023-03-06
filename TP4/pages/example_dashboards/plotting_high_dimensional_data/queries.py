import pandas as pd

from TP4.queries.base import BQBase


class BQClient(BQBase):

    def __init__(self, tenant_id):
        super().__init__("101015", retrieve_date=False)
        self.df_data = pd.read_csv("TP4/pages/example_dashboards/new_beverage_chemistry.csv")
