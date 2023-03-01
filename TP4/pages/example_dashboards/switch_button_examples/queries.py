import pandas as pd
import pandasql as ps

from TP4.queries.base import BQBase


class BQClient(BQBase):

    def __init__(self, tenant_id):
        super().__init__("101015", retrieve_date=False)
        self.vgsales_df = pd.read_csv("TP4/pages/example_dashboards/vgsales_positive.csv")

    def get_where_condition(self, filters, unwanted_fields=[None]):
        where_condition = """"""
        for key, item in filters.items():
            if key not in unwanted_fields:
                if isinstance(item, list):
                    if item != ["ALL"] and len(item) > 0:
                        if len(item) == 1:
                            cond = """('""" + str(item[0]) + """')"""
                        else:
                            cond = tuple(item)
                        where_condition += f" AND {key} IN {cond}"
                elif isinstance(item, str):
                    if item not in ["ALL", "RESET..."] and item is not None:
                        where_condition += f""" AND {key}="{item}" """
        return where_condition

    def query_sales_by_platform(self, filters):
        # Get where conditions from selector filters
        conditions = self.get_where_condition(filters)
        df = self.vgsales_df

        # Write the query that retrieved the data at each new data refresh
        query = f"""
        SELECT
            platform,
            SUM(global_sales) AS sales,
            SUM(eu_sales) AS eu_sales,
            SUM(na_sales) AS na_sales,
            SUM(jp_sales) AS jp_sales
        FROM
            df
        WHERE
            1=1
            {conditions}
        GROUP BY
            platform
        ORDER BY
            sales DESC
        """
        # Run query and store results in a pandas dataframe
        data = ps.sqldf(query)
        return data

    def query_sales_per_year(self, filters):
        # Get where conditions from selector filters
        conditions = self.get_where_condition(filters)
        df = self.vgsales_df

        # Write the query that retrieved the data at each new data refresh
        query = f"""
        SELECT
            CAST(year AS text) AS year,
            SUM(global_sales) AS sales,
            SUM(eu_sales) AS eu_sales,
            SUM(na_sales) AS na_sales,
            SUM(jp_sales) AS jp_sales
        FROM
            df
        WHERE
            1=1 AND
            year IS NOT NULL
            {conditions}
        GROUP BY
            year
        ORDER BY
            year
        """
        # Run query and store results in a pandas dataframe
        data = ps.sqldf(query)
        return data

    def get_selector_fields(self):
        df = self.vgsales_df
        query = f"""
        SELECT DISTINCT platform,
                        genre,
                        publisher

        FROM df
        """
        fields = ps.sqldf(query)

        fields = fields.append({"platform": "ALL", "genre": "ALL", "publisher": "ALL"}, ignore_index=True)

        return fields
