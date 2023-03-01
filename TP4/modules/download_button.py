import os
from io import BytesIO, StringIO

import pandas as pd
import panel as pn
import param


class FileButtonDownload(param.Parameterized):
    download = param.Action()

    def __init__(self, filename, **params):
        super().__init__(**params)
        self.data = pd.DataFrame({"1": [0, 1], "2": [1, 2]})
        self.filename = filename
        self.get_panel()

    def update_data(self, data):
        self.data = data
        if isinstance(self.data, dict):
            self.panel.callback = self.get_xlsx
            self.panel.filename = self.filename + '.xlsx'
            sio = self.get_xlsx()
        else:
            self.panel.callback = self.get_stream
            self.panel.filename = self.filename + '.csv'
            sio = self.get_stream()

    def get_stream(self):
        sio = StringIO()
        self.data.to_csv(sio)
        sio.seek(0)
        return sio

    def get_xlsx(self):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        for key in self.data:
            self.data[key].to_excel(writer, sheet_name=key[:30])
        writer.save()  # Important!
        output.seek(0)  # Important!
        return output

    def get_panel(self):
        self.panel = pn.widgets.FileDownload(callback=self.get_stream,
                                             filename=self.filename + '.csv',
                                             button_type="primary",
                                             label="DOWNLOAD DATA")
