# pylint: disable=redefined-outer-name,protected-access
# pylint: disable=missing-function-docstring,missing-modules-docstring,missing-class-docstring
# pylint: disable=line-too-long
import panel as pn
import param

DEFAULT_URL = "https://raw.githubusercontent.com/holoviz/panel/5ea166fdda6e1f958d2d9929ae2ed2b8e962156c/panel/assets/spinner_default.svg"
DARK_URL = "https://raw.githubusercontent.com/holoviz/panel/5ea166fdda6e1f958d2d9929ae2ed2b8e962156c/panel/assets/spinner_dark.svg"
# pylint: disable=enable-too-long

DEFAULT_COLOR = "#757575"
DARK_COLOR = "#BDBDBD"


def _clean(color):
    return color.replace("#", "%23")


def bar_chart_url(color):
    color = _clean(color)

    return f"""
data:image/svg+xml,
<svg xmlns="http://www.w3.org/2000/svg" style="margin: auto; background: none; display: block; shape-rendering: auto;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
<g transform="rotate(180 50 50)"><rect x="15" y="15" width="10" height="40" fill="{color}">
<animate attributeName="height" values="50;70;30;50" keyTimes="0;0.33;0.66;1" dur="1s" repeatCount="indefinite" calcMode="spline" keySplines="0.5 0 0.5 1;0.5 0 0.5 1;0.5 0 0.5 1" begin="-0.4s"></animate>
</rect><rect x="35" y="15" width="10" height="40" fill="{color}">
<animate attributeName="height" values="50;70;30;50" keyTimes="0;0.33;0.66;1" dur="1s" repeatCount="indefinite" calcMode="spline" keySplines="0.5 0 0.5 1;0.5 0 0.5 1;0.5 0 0.5 1" begin="-0.2s"></animate>
</rect><rect x="55" y="15" width="10" height="40" fill="{color}">
<animate attributeName="height" values="50;70;30;50" keyTimes="0;0.33;0.66;1" dur="1s" repeatCount="indefinite" calcMode="spline" keySplines="0.5 0 0.5 1;0.5 0 0.5 1;0.5 0 0.5 1" begin="-0.6s"></animate>
</rect><rect x="75" y="15" width="10" height="40" fill="{color}">
<animate attributeName="height" values="50;70;30;50" keyTimes="0;0.33;0.66;1" dur="1s" repeatCount="indefinite" calcMode="spline" keySplines="0.5 0 0.5 1;0.5 0 0.5 1;0.5 0 0.5 1" begin="-1s"></animate>
</rect></g></svg>
""".replace(
        "\n", ""
    )


def bars_url(color):
    color = _clean(color)

    return f"""
data:image/svg+xml,
<svg xmlns="http://www.w3.org/2000/svg" style="margin: auto; background: none; display: block; shape-rendering: auto;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
<rect x="15" y="30" width="10" height="40" fill="{color}">
  <animate attributeName="opacity" dur="1s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.5 0 0.5 1;0.5 0 0.5 1" values="1;0.2;1" begin="-0.6"></animate>
</rect><rect x="35" y="30" width="10" height="40" fill="{color}">
  <animate attributeName="opacity" dur="1s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.5 0 0.5 1;0.5 0 0.5 1" values="1;0.2;1" begin="-0.4"></animate>
</rect><rect x="55" y="30" width="10" height="40" fill="{color}">
  <animate attributeName="opacity" dur="1s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.5 0 0.5 1;0.5 0 0.5 1" values="1;0.2;1" begin="-0.2"></animate>
</rect><rect x="75" y="30" width="10" height="40" fill="{color}">
  <animate attributeName="opacity" dur="1s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.5 0 0.5 1;0.5 0 0.5 1" values="1;0.2;1" begin="-1"></animate>
</rect></svg>""".replace(
        "\n", ""
    )


def spinner_url(color):
    color = _clean(color)

    return f"""
data:image/svg+xml,
<svg xmlns="http://www.w3.org/2000/svg" style="margin: auto; background: none; display: block; shape-rendering: auto;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
<g transform="rotate(0 50 50)">
  <rect x="47" y="24" rx="3" ry="6" width="6" height="12" fill="{color}">
    <animate attributeName="opacity" values="1;0" keyTimes="0;1" dur="1s" begin="-0.9166666666666666s" repeatCount="indefinite"></animate>
  </rect>
</g><g transform="rotate(30 50 50)">
  <rect x="47" y="24" rx="3" ry="6" width="6" height="12" fill="{color}">
    <animate attributeName="opacity" values="1;0" keyTimes="0;1" dur="1s" begin="-0.8333333333333334s" repeatCount="indefinite"></animate>
  </rect>
</g><g transform="rotate(60 50 50)">
  <rect x="47" y="24" rx="3" ry="6" width="6" height="12" fill="{color}">
    <animate attributeName="opacity" values="1;0" keyTimes="0;1" dur="1s" begin="-0.75s" repeatCount="indefinite"></animate>
  </rect>
</g><g transform="rotate(90 50 50)">
  <rect x="47" y="24" rx="3" ry="6" width="6" height="12" fill="{color}">
    <animate attributeName="opacity" values="1;0" keyTimes="0;1" dur="1s" begin="-0.6666666666666666s" repeatCount="indefinite"></animate>
  </rect>
</g><g transform="rotate(120 50 50)">
  <rect x="47" y="24" rx="3" ry="6" width="6" height="12" fill="{color}">
    <animate attributeName="opacity" values="1;0" keyTimes="0;1" dur="1s" begin="-0.5833333333333334s" repeatCount="indefinite"></animate>
  </rect>
</g><g transform="rotate(150 50 50)">
  <rect x="47" y="24" rx="3" ry="6" width="6" height="12" fill="{color}">
    <animate attributeName="opacity" values="1;0" keyTimes="0;1" dur="1s" begin="-0.5s" repeatCount="indefinite"></animate>
  </rect>
</g><g transform="rotate(180 50 50)">
  <rect x="47" y="24" rx="3" ry="6" width="6" height="12" fill="{color}">
    <animate attributeName="opacity" values="1;0" keyTimes="0;1" dur="1s" begin="-0.4166666666666667s" repeatCount="indefinite"></animate>
  </rect>
</g><g transform="rotate(210 50 50)">
  <rect x="47" y="24" rx="3" ry="6" width="6" height="12" fill="{color}">
    <animate attributeName="opacity" values="1;0" keyTimes="0;1" dur="1s" begin="-0.3333333333333333s" repeatCount="indefinite"></animate>
  </rect>
</g><g transform="rotate(240 50 50)">
  <rect x="47" y="24" rx="3" ry="6" width="6" height="12" fill="{color}">
    <animate attributeName="opacity" values="1;0" keyTimes="0;1" dur="1s" begin="-0.25s" repeatCount="indefinite"></animate>
  </rect>
</g><g transform="rotate(270 50 50)">
  <rect x="47" y="24" rx="3" ry="6" width="6" height="12" fill="{color}">
    <animate attributeName="opacity" values="1;0" keyTimes="0;1" dur="1s" begin="-0.16666666666666666s" repeatCount="indefinite"></animate>
  </rect>
</g><g transform="rotate(300 50 50)">
  <rect x="47" y="24" rx="3" ry="6" width="6" height="12" fill="{color}">
    <animate attributeName="opacity" values="1;0" keyTimes="0;1" dur="1s" begin="-0.08333333333333333s" repeatCount="indefinite"></animate>
  </rect>
</g><g transform="rotate(330 50 50)">
  <rect x="47" y="24" rx="3" ry="6" width="6" height="12" fill="{color}">
    <animate attributeName="opacity" values="1;0" keyTimes="0;1" dur="1s" begin="0s" repeatCount="indefinite"></animate>
  </rect>
</g></svg>""".replace(
        "\n", ""
    )


def dual_ring_url(color):
    color = _clean(color)
    return f"""
data:image/svg+xml,
<svg xmlns="http://www.w3.org/2000/svg" style="margin: auto; background: none; display: block; shape-rendering: auto;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
<circle cx="50" cy="50" r="32" stroke-width="8" stroke="{color}" stroke-dasharray="50.26548245743669 50.26548245743669" fill="none" stroke-linecap="round">
  <animateTransform attributeName="transform" type="rotate" repeatCount="indefinite" dur="1s" keyTimes="0;1" values="0 50 50;360 50 50"></animateTransform>
</circle></svg>
""".replace(
        "\n", ""
    )


def message_url(color):
    color = _clean(color)
    return f"""
data:image/svg+xml,
<svg xmlns="http://www.w3.org/2000/svg" style="margin: auto; background: none; display: block; shape-rendering: auto;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
<g transform="translate(20 50)">
<circle cx="0" cy="0" r="6" fill="{color}">
  <animateTransform attributeName="transform" type="scale" begin="-0.375s" calcMode="spline" keySplines="0.3 0 0.7 1;0.3 0 0.7 1" values="0;1;0" keyTimes="0;0.5;1" dur="1s" repeatCount="indefinite"></animateTransform>
</circle>
</g><g transform="translate(40 50)">
<circle cx="0" cy="0" r="6" fill="{color}">
  <animateTransform attributeName="transform" type="scale" begin="-0.25s" calcMode="spline" keySplines="0.3 0 0.7 1;0.3 0 0.7 1" values="0;1;0" keyTimes="0;0.5;1" dur="1s" repeatCount="indefinite"></animateTransform>
</circle>
</g><g transform="translate(60 50)">
<circle cx="0" cy="0" r="6" fill="{color}">
  <animateTransform attributeName="transform" type="scale" begin="-0.125s" calcMode="spline" keySplines="0.3 0 0.7 1;0.3 0 0.7 1" values="0;1;0" keyTimes="0;0.5;1" dur="1s" repeatCount="indefinite"></animateTransform>
</circle>
</g><g transform="translate(80 50)">
<circle cx="0" cy="0" r="6" fill="{color}">
  <animateTransform attributeName="transform" type="scale" begin="0s" calcMode="spline" keySplines="0.3 0 0.7 1;0.3 0 0.7 1" values="0;1;0" keyTimes="0;0.5;1" dur="1s" repeatCount="indefinite"></animateTransform>
</circle>
</g></svg>
""".replace(
        "\n", ""
    )


def pulse_url(color):
    color = _clean(color)
    return f"""
data:image/svg+xml,
<svg xmlns="http://www.w3.org/2000/svg" style="margin: auto; background: none; display: block; shape-rendering: auto;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
<rect x="17.5" y="30" width="15" height="40" fill="{color}">
  <animate attributeName="y" repeatCount="indefinite" dur="1s" calcMode="spline" keyTimes="0;0.5;1" values="18;30;30" keySplines="0 0.5 0.5 1;0 0.5 0.5 1" begin="-0.2s"></animate>
  <animate attributeName="height" repeatCount="indefinite" dur="1s" calcMode="spline" keyTimes="0;0.5;1" values="64;40;40" keySplines="0 0.5 0.5 1;0 0.5 0.5 1" begin="-0.2s"></animate>
</rect>
<rect x="42.5" y="30" width="15" height="40" fill="{color}">
  <animate attributeName="y" repeatCount="indefinite" dur="1s" calcMode="spline" keyTimes="0;0.5;1" values="20.999999999999996;30;30" keySplines="0 0.5 0.5 1;0 0.5 0.5 1" begin="-0.1s"></animate>
  <animate attributeName="height" repeatCount="indefinite" dur="1s" calcMode="spline" keyTimes="0;0.5;1" values="58.00000000000001;40;40" keySplines="0 0.5 0.5 1;0 0.5 0.5 1" begin="-0.1s"></animate>
</rect>
<rect x="67.5" y="30" width="15" height="40" fill="{color}">
  <animate attributeName="y" repeatCount="indefinite" dur="1s" calcMode="spline" keyTimes="0;0.5;1" values="20.999999999999996;30;30" keySplines="0 0.5 0.5 1;0 0.5 0.5 1"></animate>
  <animate attributeName="height" repeatCount="indefinite" dur="1s" calcMode="spline" keyTimes="0;0.5;1" values="58.00000000000001;40;40" keySplines="0 0.5 0.5 1;0 0.5 0.5 1"></animate>
</rect></svg>
""".replace(
        "\n", ""
    )


def rolling_url(color):
    color = _clean(color)
    return f"""
data:image/svg+xml,
<svg xmlns="http://www.w3.org/2000/svg" style="margin: auto; background: none; display: block; shape-rendering: auto;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
<circle cx="50" cy="50" fill="none" stroke="{color}" stroke-width="10" r="35" stroke-dasharray="164.93361431346415 56.97787143782138">
  <animateTransform attributeName="transform" type="rotate" repeatCount="indefinite" dur="1s" values="0 50 50;360 50 50" keyTimes="0;1"></animateTransform>
</circle></svg>
""".replace(
        "\n", ""
    )


def spin_url(color):
    color = _clean(color)
    return f"""
data:image/svg+xml,
<svg xmlns="http://www.w3.org/2000/svg" style="margin: auto; background: none; display: block; shape-rendering: auto;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
<g transform="translate(80,50)">
<g transform="rotate(0)">
<circle cx="0" cy="0" r="6" fill="{color}" fill-opacity="1">
  <animateTransform attributeName="transform" type="scale" begin="-0.875s" values="1.5 1.5;1 1" keyTimes="0;1" dur="1s" repeatCount="indefinite"></animateTransform>
  <animate attributeName="fill-opacity" keyTimes="0;1" dur="1s" repeatCount="indefinite" values="1;0" begin="-0.875s"></animate>
</circle>
</g>
</g><g transform="translate(71.21320343559643,71.21320343559643)">
<g transform="rotate(45)">
<circle cx="0" cy="0" r="6" fill="{color}" fill-opacity="0.875">
  <animateTransform attributeName="transform" type="scale" begin="-0.75s" values="1.5 1.5;1 1" keyTimes="0;1" dur="1s" repeatCount="indefinite"></animateTransform>
  <animate attributeName="fill-opacity" keyTimes="0;1" dur="1s" repeatCount="indefinite" values="1;0" begin="-0.75s"></animate>
</circle>
</g>
</g><g transform="translate(50,80)">
<g transform="rotate(90)">
<circle cx="0" cy="0" r="6" fill="{color}" fill-opacity="0.75">
  <animateTransform attributeName="transform" type="scale" begin="-0.625s" values="1.5 1.5;1 1" keyTimes="0;1" dur="1s" repeatCount="indefinite"></animateTransform>
  <animate attributeName="fill-opacity" keyTimes="0;1" dur="1s" repeatCount="indefinite" values="1;0" begin="-0.625s"></animate>
</circle>
</g>
</g><g transform="translate(28.786796564403577,71.21320343559643)">
<g transform="rotate(135)">
<circle cx="0" cy="0" r="6" fill="{color}" fill-opacity="0.625">
  <animateTransform attributeName="transform" type="scale" begin="-0.5s" values="1.5 1.5;1 1" keyTimes="0;1" dur="1s" repeatCount="indefinite"></animateTransform>
  <animate attributeName="fill-opacity" keyTimes="0;1" dur="1s" repeatCount="indefinite" values="1;0" begin="-0.5s"></animate>
</circle>
</g>
</g><g transform="translate(20,50.00000000000001)">
<g transform="rotate(180)">
<circle cx="0" cy="0" r="6" fill="{color}" fill-opacity="0.5">
  <animateTransform attributeName="transform" type="scale" begin="-0.375s" values="1.5 1.5;1 1" keyTimes="0;1" dur="1s" repeatCount="indefinite"></animateTransform>
  <animate attributeName="fill-opacity" keyTimes="0;1" dur="1s" repeatCount="indefinite" values="1;0" begin="-0.375s"></animate>
</circle>
</g>
</g><g transform="translate(28.78679656440357,28.786796564403577)">
<g transform="rotate(225)">
<circle cx="0" cy="0" r="6" fill="{color}" fill-opacity="0.375">
  <animateTransform attributeName="transform" type="scale" begin="-0.25s" values="1.5 1.5;1 1" keyTimes="0;1" dur="1s" repeatCount="indefinite"></animateTransform>
  <animate attributeName="fill-opacity" keyTimes="0;1" dur="1s" repeatCount="indefinite" values="1;0" begin="-0.25s"></animate>
</circle>
</g>
</g><g transform="translate(49.99999999999999,20)">
<g transform="rotate(270)">
<circle cx="0" cy="0" r="6" fill="{color}" fill-opacity="0.25">
  <animateTransform attributeName="transform" type="scale" begin="-0.125s" values="1.5 1.5;1 1" keyTimes="0;1" dur="1s" repeatCount="indefinite"></animateTransform>
  <animate attributeName="fill-opacity" keyTimes="0;1" dur="1s" repeatCount="indefinite" values="1;0" begin="-0.125s"></animate>
</circle>
</g>
</g><g transform="translate(71.21320343559643,28.78679656440357)">
<g transform="rotate(315)">
<circle cx="0" cy="0" r="6" fill="{color}" fill-opacity="0.125">
  <animateTransform attributeName="transform" type="scale" begin="0s" values="1.5 1.5;1 1" keyTimes="0;1" dur="1s" repeatCount="indefinite"></animateTransform>
  <animate attributeName="fill-opacity" keyTimes="0;1" dur="1s" repeatCount="indefinite" values="1;0" begin="0s"></animate>
</circle>
</g>
</g></svg>
""".replace(
        "\n", ""
    )


SPINNERS = {
    "Default": DEFAULT_URL,
    "Dark": DARK_URL,
    "Bar Chart": bar_chart_url,
    "Bars": bars_url,
    "Dual Ring": dual_ring_url,
    "Message": message_url,
    "Pulse": pulse_url,
    "Rolling": rolling_url,
    "Spin": spin_url,
    "Spinner": spinner_url,
}


class LoadingStyler(param.Parameterized):
    """A utility that can be used to select and style the loading spinner"""

    spinner = param.ObjectSelector(
        default=DEFAULT_URL, objects=SPINNERS, doc="The loading spinner to use"
    )
    spinner_height = param.Integer(50, bounds=(1, 100))
    background_rgb = param.Tuple((255, 255, 255))
    background_alpha = param.Number(
        0.5, bounds=(0.0, 1.0), step=0.01, doc="The background alpha"
    )
    color = param.Color(DEFAULT_COLOR)
    style = param.String("", doc="The CSS Style applied to the loading spinner")

    settings_panel = param.Parameter(
        doc="A panel containing the settings of the LoadingStyler"
    )
    style_panel = param.Parameter(
        doc="An 'invisible' HTML pane containing the css style"
    )

    def __init__(self, **params):
        super().__init__(**params)

        self.settings_panel = pn.Param(
            self,
            parameters=[
                "spinner",
                "spinner_height",
                "background_alpha",
                "color",
                "style",
            ],
            widgets={
                "style": {
                    "type": pn.widgets.TextAreaInput,
                    "sizing_mode": "stretch_both",
                    "disabled": True,
                }
            },
        )

        self.style_panel = pn.pane.HTML(
            sizing_mode="fixed", width=0, height=0, margin=0
        )
        self._toggle_color()
        self._update_style()

    @property
    def _spinner_url(self):
        spinner = self.spinner
        if callable(spinner):
            return spinner(self.color)  # pylint: disable=not-callable
        return spinner

    @param.depends("spinner", watch=True)
    def _toggle_color(self):
        color_picker: pn.widgets.ColorPicker = [
            widget
            for widget in self.settings_panel
            if isinstance(widget, pn.widgets.ColorPicker)
        ][0]
        color_picker.disabled = not callable(self.spinner)

    @param.depends(
        "spinner",
        "spinner_height",
        "color",
        "background_rgb",
        "background_alpha",
        watch=True,
    )
    def _update_style(self):
        self.style = f"""
.bk.pn-loading.arcs:before {{
background-image: url('{self._spinner_url}');
background-size: auto {self.spinner_height}%;
background-color: rgb({self.background_rgb[0]},{self.background_rgb[1]},{self.background_rgb[2]},{self.background_alpha});
}}"""

    @param.depends("style", watch=True)
    def _update_loading_spinner_css(self):
        self.style_panel.object = f"""<style>{self.style}</style>"""
