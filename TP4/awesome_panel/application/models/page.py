"""This module implements the Page Model"""
import param

from TP4.awesome_panel.application.models.author import Author
from TP4.awesome_panel.utils import OrderByNameMixin


class Page(OrderByNameMixin, param.Parameterized):
    """This Page Model contains the

    - page component (For example a PageComponent)
    - meta parameters like author and description"""

    author = param.ClassSelector(class_=Author, allow_None=True)
    description = param.String()
    tags = param.List()
    source_code_url = param.String()
    thumbnail_png_url = param.String()
    component = param.Parameter()
    show_loading_page = param.Boolean(default=False)
    restrict_max_width = param.Boolean(default=True)
    url = param.String()

    def __hash__(
        self,
    ):
        return hash(self.name)
