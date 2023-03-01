import panel as pn
import param

from TP4.modules.base.base_selector import BaseSelector
from TP4.pages.example_dashboards.switch_button_examples.queries import BQClient


class VGSelector(BaseSelector):
    platform = param.ListSelector(default=["ALL"], objects=["ALL"])
    genre = param.ListSelector(default=["ALL"], objects=["ALL"])
    publisher = param.ListSelector(default=["ALL"], objects=["ALL"])

    def __init__(self, BQHandler: BQClient, **params):
        self.BQHandler = BQHandler
        
        self.distinct_fields = self.BQHandler.get_selector_fields()
        print(f"The fileds are {self.distinct_fields}")
        self.build_distinct_fields(self.distinct_fields)
        super().__init__(**params)

        self.settings_panel = pn.Param(
            self,
            name="",
            parameters=[
                "platform",
                "genre",
                "publisher",
            ],
            widgets={
                "platform": {"type": pn.widgets.MultiChoice},
                "genre": {"type": pn.widgets.MultiChoice},
                "publisher": {"type": pn.widgets.MultiChoice},
            },
        )

    def get_filters(self):
        platform_val = self.platform
        genre_val = self.genre
        publisher_val = self.publisher
        dict_values = {
            "platform": platform_val,
            "genre": genre_val,
            "publisher": publisher_val,
        }
        filters = {}
        for key, val in dict_values.items():
            if "ALL" not in val:
                filters[key] = val
        return filters

    @param.depends(
        "platform",
        "genre",
        "publisher",
        watch=True,
    )
    def update_fields(self):
        self.loading = True
        filters = self.get_filters()
        df = self.distinct_fields
        for key, input in filters.items():
            if input != "ALL":
                df = df[df[key].isin(input)]

        self.build_distinct_fields(df)
        self.loading = False
        return True

    def build_distinct_fields(self, df):
        self.param.platform.objects = ["ALL"] + list(df["platform"].unique())
        self.param.genre.objects = ["ALL"] + list(df["genre"].unique())
        self.param.publisher.objects = ["ALL"] + list(df["publisher"].unique())
