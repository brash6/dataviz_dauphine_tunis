"""# PandasProfileReport

The PandasProfileReport pane enables a user to show a ProfileReport generated by the
[Pandas profile_report](https://github.com/pandas-profiling/pandas-profiling) package.
"""
import html

import panel as pn
import param
from pandas_profiling import ProfileReport

# pylint: disable=line-too-long
OBJECT_WHEN_LOADING_REPORT_REPORT = (
    "<p class='pandas-profile-report-loading'>Loading Report ...</p>"
)
GREEN = "#174c4f"
ORANGE = "#cc5c29"
LOGO_URL = "https://raw.githubusercontent.com/MarcSkovMadsen/awesome-panel/master/application/pages/pandas_profiling_app/pandas_profiler_logo.png"
# pylint: enable=line-too-long
STYLE = "width:100%;height:100%;"
OBJECT_WHEN_NO_REPORT = "<p class='pandas-profile-report-no-report'>No Report Available</p>"


class PandasProfileReport(pn.pane.HTML):
    """The PandasProfilingApp showcases how to integrate the Pandas Profiling Report with Panel"""

    profile_report = param.ClassSelector(class_=ProfileReport)
    object_when_loading_report = param.String(OBJECT_WHEN_LOADING_REPORT_REPORT)
    object_when_no_report = param.String(OBJECT_WHEN_NO_REPORT)

    # In order to not be selected by the `pn.panel` selection process
    # Cf. https://github.com/holoviz/panel/issues/1494#issuecomment-663219654
    priority = 0
    # The _rename dict is used to keep track of Panel parameters to sync to Bokeh properties.
    # As value is not a property on the Bokeh model we should set it to None
    _rename = dict(pn.pane.HTML._rename, profile_report=None)

    def __init__(self, **params):
        super().__init__(**params)

        self._update_object_from_parameters()

    # Don't name the function
    # `_update`, `_update_object`, `_update_model` or `_update_pane`
    # as this will override a function in the parent class.
    @param.depends("profile_report", "object_when_no_report", watch=True)
    def _update_object_from_parameters(self):
        if not self.profile_report:
            self.object = self.object_when_no_report
            return

        self.object = self.object_when_loading_report
        self.object = self._to_html(self.profile_report)

    @staticmethod
    def _to_html(profile_report: ProfileReport) -> str:
        html_report = profile_report.to_html()
        html_report = html.escape(html_report)
        return (
            f'<iframe srcdoc="{html_report}" style={STYLE} frameborder="0" '
            "allowfullscreen></iframe>"
        )

    def __str__(self):
        return "Pandas Profile Report"

    def __repr__(self, depth: int = 1):
        return self.__str__()
