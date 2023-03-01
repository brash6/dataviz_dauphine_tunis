
from bokeh.models import (
    CellFormatter,
    FuncTickFormatter,
    HTMLTemplateFormatter,
    NumeralTickFormatter,
)

countries_ending_currency = ['BEL', 'ESP', 'FRA', 'ITA', 'POL', 'ROU']


def currency_mapper(country, currency_selected):
    currency = "€"
    currency_code = "EUR"
    if not currency_selected == "EUR":
        if country == "BRA":
            currency = "R$"
            currency_code = "BRL"
        if country == "POL":
            currency = "zł"
            currency_code = "PLN"
        if country == "ROU":
            currency = "lei"
            currency_code = "RON"
        if country == "TWN":
            currency = "NT$"
            currency_code = "TWD"
        if country == "ARG":
            currency = "$"
            currency_code = "ARS"
    return currency, currency_code

import numpy as np
from bokeh.models import FuncTickFormatter, NumeralTickFormatter
from numerize import numerize


def currency_mapper(country, currency_selected):
    currency = "€"
    currency_code = "EUR"
    if not currency_selected == "EUR":
        if country == "BRA":
            currency = "R$"
            currency_code = "BRL"
        if country == "POL":
            currency = "zł"
            currency_code = "PLN"
        if country == "ROU":
            currency = "lei"
            currency_code = "RON"
        if country == "TWN":
            currency = "NT$"
            currency_code = "TWD"
        if country == "ARG":
            currency = "$"
            currency_code = "ARS"
        if country == "GBR":
            currency = "£"
            currency_code = "GBP"
    return currency, currency_code


def conditional_coloring(val, cutoff, colors):
    i = 0
    for cutoff_values in cutoff:
        if val < cutoff_values:
            return colors[i]
        i += 1
    return colors[-1]


def format_label(num):
    num = float(num)
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return "%.1f%s" % (num, ["", "K", "M", "B"][magnitude])


def format_label_euro(val):
    val = float(val)
    magnitude = 0
    while abs(val) >= 1000:
        magnitude += 1
        val /= 1000.0
    return "%.1f%s" % (val, ["€", "K€", "M€", "B€"][magnitude])


def override_numerize(n, decimals=2):
    if np.isnan(n):
        return str(n)
    else:
        return numerize.numerize(n, decimals)


OVERLAPPING_BARPLOT_Y_AXIS_FORMATTER = FuncTickFormatter(code="""
                                             if (Math.abs(tick) < 1e3)
                                             {
                                                var unit = ''
                                                var num =  (tick).toFixed(1)
                                             }
                                             else if (Math.abs(tick) < 1e6)
                                             {
                                                var unit = 'K'
                                                var num =  (tick/1e3).toFixed(1)
                                             }
                                             else if (Math.abs(tick) < 1e9)
                                             {
                                                var unit = 'M'
                                                var num =  (tick/1e6).toFixed(1)
                                             }
                                             else
                                             {
                                                var unit = 'B'
                                                var num =  (tick/1e9).toFixed(1)
                                             }
                                             return `${num}${unit}`""")

NEW_Y_AXIS_FORMATTER = FuncTickFormatter(code="""
                                             if (Math.abs(tick) < 1)
                                             {
                                                var unit = ''
                                                var num =  (tick).toFixed(1)
                                             }
                                             if (Math.abs(tick) < 1e3)
                                             {
                                                var unit = ''
                                                var num =  (tick).toFixed(0)
                                             }
                                             else if (Math.abs(tick) < 1e6)
                                             {
                                                var unit = 'K'
                                                var num =  (tick/1e3).toFixed(1)
                                             }
                                             else if (Math.abs(tick) < 1e9)
                                             {
                                                var unit = 'M'
                                                var num =  (tick/1e6).toFixed(1)
                                             }
                                             else
                                             {
                                                var unit = 'B'
                                                var num =  (tick/1e9).toFixed(1)
                                             }
                                             return `${num}${unit}`""")

NEW_Y_AXIS_FORMATTER_P = FuncTickFormatter(code="""
                                            var unit = '%'
                                            var num =  (tick).toFixed(0)
                                            return `${num}${unit}`""")

OVERLAPPING_BARPLOT_Y_AXIS_EURO_FORMATTER = FuncTickFormatter(code="""if (Math.abs(tick) < 1e3)
                                             {
                                                var unit = ''
                                                var num =  (tick).toFixed(0)
                                             }
                                             else if (Math.abs(tick) < 1e6)
                                             {
                                                var unit = 'K'
                                                var num =  (tick/1e3).toFixed(1)
                                             }
                                             else
                                             {
                                                var unit = 'M'
                                                var num =  (tick/1e6).toFixed(1)
                                             }
                                             return `€ ${num}${unit}`""")


def currency_y_axis_formatter(currency_symbol):
    return FuncTickFormatter(code=f"""if (Math.abs(tick) < 1e3)
                                                 {{
                                                    var unit = ''
                                                    var num =  (tick).toFixed(0)
                                                 }}
                                                 else if (Math.abs(tick) < 1e6)
                                                 {{
                                                    var unit = 'K'
                                                    var num =  (tick/1e3).toFixed(1)
                                                 }}
                                                 else
                                                 {{
                                                    var unit = 'M'
                                                    var num =  (tick/1e6).toFixed(1)
                                                 }}
                                                 return `{currency_symbol} ${{num}}${{unit}}`""")


SIMPLE_BARPLOT_FORMATTER = FuncTickFormatter(
    code="""if (tick < 1e3)
                                             {
                                                var unit = ''
                                                var num =  (tick).toFixed(0)
                                             }
                                             else if (Math.abs(tick) < 1e6)
                                             {
                                                var unit = 'K'
                                                var num =  (tick/1e3).toFixed(1)
                                             }
                                             else
                                             {
                                                var unit = 'M'
                                                var num =  (tick/1e6).toFixed(1)
                                             }
                                             return `${num}${unit}`"""
)

MSMT_SIMPLE_BARPLOT_FORMATTER = FuncTickFormatter(
    code="""if (tick < 1e3)
                                             {
                                                var unit = ''
                                                var num =  (tick).toFixed(0)
                                             }
                                             else if (Math.abs(tick) < 1e6)
                                             {
                                                var unit = 'K'
                                                var num =  (tick/1e3).toFixed(0)
                                             }
                                             else
                                             {
                                                var unit = 'M'
                                                var num =  (tick/1e6).toFixed(0)
                                             }
                                             return `${num}${unit}`"""
)

IYA_BARPLOT_Y_AXIS_FORMATTER = FuncTickFormatter(
    code="""var num = (tick).toFixed(1); return `${num}`"""
)

DATA_TABLE_FORMATTER = """<div style="text-align:center;
                           background: <%=(function colorfromint(){{if({0} >= 100)
                           {{return("#56AA4E")}} else {{return "#960F05"}} }}())%>;
                           color: <%=(function colorfromint(){{return("white")}}())  %>;"><%= value %>
                          </div>"""

TABULATOR_FORMATTER_IYA = """<div style="background: <%
                                if (value >= 100) {
                                    %>#56AA4E<%
                                } else {
                                    %>#960F05<%
                                } %>; color: white;">
                                <%- value %>
                            </div>
                           """

TABULATOR_FORMATTER_MONITORING = """<div style="background: <%
                                if (value == true) {
                                    %>#56AA4E<%
                                } else {
                                    %>#960F05<%
                                } %>; color: white;">
                                <%- value %>
                            </div>
                           """

TABULATOR_FORMATTER_IYA_V2 = """<div style="text-align:center;
                                background: <%
                                if (value >= 100) {
                                    %>#56AA4E<%
                                } else {
                                    %>#960F05<%
                                } %>; color: white;">
                                <%- value %>
                            </div>
                           """

TABULATOR_FORMATTER_DYA = """<div style="background: <%
                                if (value >= 0) {
                                    %>#56AA4E<%
                                } else {
                                    %>#960F05<%
                                } %>; color: white;">
                                <%- value %>
                            </div>
                           """

TABULATOR_FORMATTER_DYA_V2 = '''<div style="text-align:center; background: <% if (value >= 0) {
                                    %>#56AA4E<%
                                } else {
                                    %>#960F05<%
                                } %>; color: white;">
                                <%- value.toLocaleString("en-US") %>
                            </div>'''

TABULATOR_FORMATTER_CODE = '<code><%= value %></code>'

DYA_DATA_TABLE_FORMATTER = """<div style="text-align:center;
                           background: <%=(function colorfromint(){{if({0} >= 0)
                           {{return("#56AA4E")}} else {{return "#960F05"}} }}())%>;
                           color: <%=(function colorfromint(){{return("white")}}())  %>;"><%= value %>
                          </div>"""

DYA_DATA_TABLE_FORMATTER_V2 = '<div style="text-align:center; background: <%=(function colorfromint(){{if({0} >= 0.5)' \
                              '{{return ("#56AA4E")}} else if ({0} <= 0) {{return "#960F05"}} else if ({0} > 0 && {0} < 0.5) ' \
                              '{{return "#BDBDBD"}} }}())%>; color: <%=(function colorfromint(){{return("white")}}())  %>;">' \
                              '<%= value.toLocaleString("en-US") %></div>'

MSMT_DATA_TABLE_FORMATTER = """<div style="text-align:center;
                           background: <%=(function colorfromint(){{if({0} >= 0)
                           {{return("#ABC984")}} else {{return "#eb989e"}} }}())%>;
                           color: <%=(function colorfromint(){{return("white")}}())  %>;"><%= (value<=0?"":"+") + (100*value).toFixed(2) + '%' %>
                          </div>"""

MSMT_DATA_TABLE_PVALUE_FORMATTER = """<div style="text-align:center;
                           background:<%=color%>"; color="white";">
                           <%= (value<=0?"":"+") + (100*value).toFixed(2) + '%' %>
                          </div>"""


def msmt_monetary_data_table_formatter(val, currency_symbol):
    html_formatter = f"""<div style="text-align:center;">
           <%= '{currency_symbol}' + (+value.toFixed(0)).toLocaleString('en-CA') %>
           </div>"""
    return HTMLTemplateFormatter(template=html_formatter.format(val))


def msmt_monetary_dec_data_table_formatter(val, currency_symbol):
    html_formatter = f"""<div style="text-align:center;">
           <%= '{currency_symbol}' + value.toFixed(2) %>
           </div>"""
    return HTMLTemplateFormatter(template=html_formatter.format(val))


STACKED_BARPLOT_FORMATTER = NumeralTickFormatter(format="0.0a")


def format_number_to_string(value, value_format=None, country=None):
    currency = currency_mapper(country, 'local')[0]

    if value_format == 'number':
        magnitude = 0
        while abs(value) >= 1000:
            magnitude += 1
            value /= 1000.0
        value = f'{value:.1f} {["", "K", "M", "B"][magnitude]}'

    elif value_format == 'number_no_dec':
        magnitude = 0
        while abs(value) >= 1000:
            magnitude += 1
            value /= 1000.0
        value = f'{value:.0f} {["", "K", "M", "B"][magnitude]}'

    elif value_format == 'full_number_plus':
        value = f'{value:+03,.0f}'

    elif value_format == 'monetary':
        magnitude = 0
        while abs(value) >= 1000:
            magnitude += 1
            value /= 1000.0
        if country in countries_ending_currency:
            value = f'{value:.1f} {["", "K", "M", "B"][magnitude]}{currency}'
        else:
            value = f'{currency}{value:.1f} {["", "K", "M", "B"][magnitude]}'

    elif value_format == 'full_monetary_plus':
        if country in countries_ending_currency:
            value = f'{value:+0,.0f}{currency} '
        else:
            value = f'{currency}{value:+0,.0f} '

    elif value_format == 'full_monetary':
        if country in countries_ending_currency:
            value = f'{value:03,.0f}{currency} '
        else:
            value = f'{currency}{value:03,.0f} '

    elif value_format == 'monetary_dec':
        if country in countries_ending_currency:
            value = f'{value:.2f}{currency}'
        else:
            value = f'{currency}{value:.2f}'

    elif value_format == 'monetary_dec_plus':
        if country in countries_ending_currency:
            value = f'{value:+03,.2f}{currency} '
        else:
            value = f'{currency}{value:+03,.2f} '

    elif value_format == 'decimal':
        value = f'{value:.2f}'

    elif value_format == 'percentage':
        value = f'{value:.1%}'

    elif value_format == 'percentage_symbol':
        value = f'{value:.1f}%'

    elif value_format == 'percentage_round':
        value = f'{value:.0%}'

    elif value_format == 'percentage_plus':
        value = f'{value:+03,.2%}'

    elif value_format == 'iya':
        value = f'{value*100:.1f}'

    value_text = str(value)

    return value_text
