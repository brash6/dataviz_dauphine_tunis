"""The Awesome Panel Gallery based on the Fast Components"""
# pylint: disable=line-too-long
import panel as pn

from TP4.utils.view import get_template
from TP4.awesome_panel_extensions.site import site
from TP4.awesome_panel_extensions.site.gallery import GalleryTemplate

APPLICATION = site.create_application(
    url="example_dashboards",
    name="Example Dashboards",
    # description="""A custom Panel template using the Fast web components""",
    # description_long="""The Gallery provides a very visual overview to the applications and associated
    # resources""",
    thumbnail="https://www.espacemanager.com/sites/default/files/field/image/nouveau_logo_universite_dauphine_tunis.jpg",
    folder="main"
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
        site="Example Dashboards",
        title="",
        # description="""The purpose of the Awesome Panel Gallery is to inspire and help you create awesome analytics apps in <fast-anchor href="https://panel.holoviz.org" target="_blank" appearance="hypertext">Panel</fast-anchor> using the tools you know and love.""",
        applications=get_app(site.applications, "example_dashboards"),
        target="_self",
        theme="default",
    )


if __name__.startswith("bokeh"):
    view().servable()
