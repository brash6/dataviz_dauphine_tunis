"""This module contains a navigation menu to be used to select between different pages"""
from typing import List, Optional, Union

import panel as pn

import TP4.awesome_panel.express as pnx


class NavigationButton(pn.widgets.Button):
    """## Navigation_Button"""

    def __init__(
        self,
        page: Union[
            pn.layout.Panel,
            pn.pane.Pane,
            pn.widgets.Widget,
        ],
        page_outlet: pn.layout.ListPanel,
        **kwargs,
    ):
        """## Navigation Button to navigate between pages

        Arguments:
            page {Union[pn.layout.Panel, pn.pane.Pane, pn.pane.Widget]} -- A page to navigate to
            when the button is clicked
            page_outlet {pn.layout.ListPanel} -- The ListPanel to update when the user navigates to
            a new page
        """
        if callable(page):
            page_ = page()
        else:
            page_ = page

        if "name" not in kwargs:
            if "css_classes" in kwargs:
                kwargs["name"] = " " + page_.name
            else:
                kwargs["name"] = page_.name
        if "width" not in kwargs:
            kwargs["width"] = 165
        super().__init__(**kwargs)

        def navigate_to_page(
            event,
        ):  # pylint: disable=unused-argument
            page_outlet[:] = [pnx.spinners.DefaultSpinner().center()]
            page_outlet[:] = [page_]

        self.on_click(navigate_to_page)


class NavigationMenu(pn.Column):
    "## Navigation Menu"

    def __init__(  # pylint: disable=too-many-arguments
        self,
        pages: List[
            Union[
                pn.layout.Panel,
                pn.pane.Pane,
            ]
        ],
        page_outlet: pn.layout.ListPanel,
        *args,
        css_classes: Optional[List[Optional[List[str]]]] = None,
        title: str = "",
        sizing_mode: str = "stretch_width",
        **kwargs,
    ):
        """## Navigation Menu

        A widget composed of NavigationButtons that can be used to navigate between pages.

        Arguments:
            pages {List[Union[pn.layout.Panel, pn.pane.Pane]]} -- A list of 'pages' to navigate
                between. The first page in pages is selected by default.
            page_outlet {pn.layout.ListPanel} -- The ListPanel to update when the user navigates to
                a new page
        """
        if css_classes:
            pnx.fontawesome.extend()
            menuitems = [
                NavigationButton(
                    page,
                    page_outlet=page_outlet,
                    css_classes=css,
                )
                for page, css in zip(
                    pages,
                    css_classes,
                )
            ]
        else:
            menuitems = [
                NavigationButton(
                    page=page,
                    page_outlet=page_outlet,
                )
                for page in pages
            ]

        # title = pnx.SubHeader(title, text_align=text_align)
        title = pn.layout.HSpacer(height=20)
        super().__init__(
            title,
            *menuitems,
            sizing_mode=sizing_mode,
            *args,
            **kwargs,
        )

        page_outlet.clear()
        page_outlet.append(pages[0])
