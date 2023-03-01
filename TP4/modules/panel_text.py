import panel as pn


class PanelText:

    def __init__(self, text="""## Panel Text primitive <hr> You can customize this text""", alert_type="light",
                 about=False, background=None, date=None, cardholder=None):
        new_text = text
        if cardholder is None:
            cardholder_text = ''
        else:
            if cardholder:
                cardholder_text = """<p style='text-align: left;'><i> This Dashboard uses cardholder info </i></p>"""
            else:
                cardholder_text = """<p style='text-align: left;'><i> This Dashboard doesn't use cardholder info </i></p>"""
        if about:
            text = f"""<p class="date-refresh"> Last data update was made on Novembre 2022 </p>""" \
                   + cardholder_text \
                   + text

            new_text = ''
            for line in text.splitlines():
                new_text = new_text + "\n" + line.lstrip()

            self.str_pane = pn.pane.Markdown(new_text, style={'font-size': '10pt', 'overflow': 'auto'})
            self.panel = pn.Card(self.str_pane, title='About this dashboard')

        else:
            if background is not None:
                self.panel = pn.pane.Alert(new_text, alert_type=alert_type, background=background)
            else:
                self.panel = pn.pane.Alert(new_text, alert_type=alert_type)

    def change_text(self, text):
        self.panel.object = text
