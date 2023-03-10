"""This module provides often utility functionality needed when working with HoloViews"""
import holoviews as hv


def _disable_logo_func(plot, _):
    plot.state.toolbar.logo = None


def disable_bokeh_logo():
    """Removes the Bokeh logo from all plots generated by HoloViews after the function has run"""
    plot = hv.plotting.bokeh.ElementPlot
    if (
        _disable_logo_func not in plot.hooks
    ):  # pylint: disable=unsupported-membership-test
        plot.hooks.append(_disable_logo_func)
