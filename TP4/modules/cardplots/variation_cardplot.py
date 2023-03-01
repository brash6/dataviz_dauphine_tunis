import panel as pn

from TP4.modules.base.base_plot import BasePlot


class VariationCardPlot(BasePlot):

    def __init__(self, title, displayed_value, second_value, second_text, **params):
        super().__init__(**params)

        self.title = title
        self.displayed_value = displayed_value
        self.second_value = second_value
        self.second_text = second_text

        self.card_html = f"""
        <div class="card-title">
        <h3>{self.title}</h3>
        </div>

        <div class="card-data">
        <h1>{self.displayed_value}</h1>
        </div>

        <div class="card-second">
        <h3>{self.second_value} {self.second_text}</h1>
        </div>
        """

        self.card_css = f"""
        div.card-title h3 {"{"}
          font-size: 14px;
          font-weight: 300;
          font-family: 'Open Sans', sans-serif;
          margin-left: 2%;
        {"}"}

        div.card-data h1 {"{"}
          font-size: 32px;
          font-weight: 400;
          font-family: 'Open Sans';
          text-align: center;
        {"}"}

        div.card-second h3 {"{"}
          font-size: 14px;
          font-weight: 300;
          font-family: 'Open Sans', sans-serif;
          text-align: center;
        {"}"}
        """

        pn.extension(raw_css=[self.card_css])
        self.panel = pn.pane.HTML(self.card_html,
                                  style={'background-color': 'white',
                                         'box-shadow': 'rgba(0, 0, 0, 0.18) 0px 2px 4px',
                                         'border-radius': '5px',
                                         'padding': '10px'})

    def update_card(self, displayed_value, second_value, background_color="white"):
        self.displayed_value = displayed_value
        self.second_value = second_value
        self.card_html = f"""
                <div class="card-title">
                <h3>{self.title}</h3>
                </div>

                <div class="card-data">
                <h1>{self.displayed_value}</h1>
                </div>

                <div class="card-second">
                <h3>{self.second_value} {self.second_text}</h1>
                </div>
                """
        self.card_css = f"""
                div.card-title h3 {"{"}
                  font-size: 14px;
                  font-weight: 300;
                  font-family: 'Open Sans', sans-serif;
                  margin-left: 2%;
                {"}"}

                div.card-data h1 {"{"}
                  font-size: 32px;
                  font-weight: 400;
                  font-family: 'Open Sans';
                  font-style: normal;
                  text-align: center;
                {"}"}

                div.card-second h3 {"{"}
                  font-size: 14px;
                  font-weight: 300;
                  font-family: 'Open Sans', sans-serif;
                  text-align: center;
                {"}"}
                """

        pn.extension(raw_css=[self.card_css])
        return pn.pane.HTML(self.card_html,
                            style={'background-color': background_color,
                                   'box-shadow': 'rgba(0, 0, 0, 0.18) 0px 2px 4px',
                                   'border-radius': '5px',
                                   'padding': '10px'})
