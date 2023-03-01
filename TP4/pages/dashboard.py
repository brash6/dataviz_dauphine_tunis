"""The Awesome Panel Gallery based on the Fast Components"""
# pylint: disable=line-too-long
import panel as pn

from TP4.utils.view import get_template
from TP4.awesome_panel_extensions.site import site
from TP4.awesome_panel_extensions.site.gallery import GalleryTemplate

APPLICATION = site.create_application(
    url="",
    name="HomePage",
    description="""The Mother of All Dashboards""",
    description_long="""This page is the main folder of all dashboards""",
    folder="origin"
)


def get_app(applications, folder):
    list_relevant_app = []
    for app in applications:
        if hasattr(app, "folder"):
            if app.folder == folder:
                list_relevant_app.append(app)
    return list_relevant_app


@site.add(APPLICATION)
def view():
    """Return a GalleryTemplate"""
    pn.config.raw_css = [
        css for css in pn.config.raw_css if not css.startswith("/* CUSTOM TEMPLATE CSS */")
    ]
    return GalleryTemplate(
        site="SafeHaven",
        title="Analytics Library",
        background_image="http://lestroisjardins.fr/wp-content/uploads/2016/04/White-header-background-1.jpg",
        description="""""",
        applications=get_app(site.applications, "main"),
        target="_self",
        theme="default",
    )


if __name__.startswith("bokeh"):
    view().servable()
