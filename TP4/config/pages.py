"""In this modules we define and register all Pages in the application

Please note that all pages in the list

- be located in https://raw.githubusercontent.com/MarcSkovMadsen/awesome-panel/master/
application/gallery
"""
from application import pages

# from TP4.pages import bootstrap_dashboard, custom_bokeh_model
from TP4.config import tags
from TP4.config.settings import GITHUB_BLOB_MASTER_URL, THUMBNAILS_ROOT
from TP4.awesome_panel.application.models import Page

GITHUB_PAGE_URL = GITHUB_BLOB_MASTER_URL + "application/pages/"

HOME = Page(
    name="Home",
    source_code_url=GITHUB_PAGE_URL + "home/home.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "home.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
    ],
    component=pages.home,
    url="",
)
ABOUT = Page(
    name="About",
    source_code_url=GITHUB_PAGE_URL + "about/about.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "about.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
    ],
    component=pages.about,
    url="about",
)
ISSUES = Page(
    name="Issues",
    source_code_url=GITHUB_PAGE_URL + "issues/issues.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "issues.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
    ],
    component=pages.issues,
    url="issues",
)
# ASYNC_TASKS = Page(
#     name="Async Tasks",
#     source_code_url=GITHUB_PAGE_URL + "async_tasks/async_tasks.py",
#     thumbnail_png_url=THUMBNAILS_ROOT + "async_tasks.png",
#     tags=[
#         tags.CODE,
#         tags.APP_IN_GALLERY,
#     ],
#     component=pages.async_tasks,
#     author=authors.JOCHEM_SMIT,
#     url="async-tasks",
# )
BOOTSTRAP_DASHBOARD = Page(
    name="Bootstrap Dashboard",
    source_code_url=GITHUB_PAGE_URL + "bootstrap_dashboard/main.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "bootstrap_dashboard.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
    ],
    component=pages.bootstrap_dashboard,
    url="bootstrap-dashboard",
)
CUSTOM_BOKEH_MODEL = Page(
    name="Custom Bokeh Model",
    source_code_url=GITHUB_PAGE_URL + "custom_bokeh_model/custom.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "custom_bokeh_model.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
    ],
    component=pages.custom_bokeh_model,
    url="custom-bokeh-model",
)
DASHBOARD = Page(
    name="Classic Dashboard",
    source_code_url=GITHUB_PAGE_URL + "dashboard/dashboard.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "dashboard.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
    ],
    component=application.pages.example_dashboards.example_dashboard.dashboard,
    show_loading_page=True,
    url="classic-dashboard",
)
DATA_EXPLORER = Page(
    name="DataExplorer - Loading...",
    source_code_url=GITHUB_PAGE_URL + "dataexplorer_loading/dataexplorer_loading.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "dataexplorer_loading.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
    ],
    component=pages.dataexplorer_loading,
    url="data-explorer-loading",
)
DETR = Page(
    name="DE:TR: Object Detection",
    source_code_url=GITHUB_PAGE_URL + "detr/detr.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "detr.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
    ],
    component=pages.detr,
    show_loading_page=True,
    url="detr",
)
IMAGE_CLASSIFIER = Page(
    name="Image Classifier",
    source_code_url=GITHUB_PAGE_URL + "image_classifier/image_classifier.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "image_classifier.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
    ],
    component=pages.image_classifier,
    url="image-classifier",
)
JS_ACTIONS = Page(
    name="JS Actions",
    source_code_url=GITHUB_PAGE_URL + "js_actions/js_actions.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "js_actions.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
    ],
    component=pages.js_actions,
    url="js-actions",
)
KICKSTARTER_DASHBOARD = Page(
    name="Kickstarter Dashboard",
    source_code_url=GITHUB_PAGE_URL + "kickstarter_dashboard/main.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "kickstarter_dashboard.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
    ],
    component=pages.kickstarter_dashboard,
    show_loading_page=True,
    url="kick-starter-dashboard",
)
OWID_CHOROPLETH_MAP = Page(
    name="Owid Choropleth Map",
    source_code_url=GITHUB_PAGE_URL + "owid_choropleth_map/main.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "owid_choropleth_map.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
    ],
    component=pages.owid_choropleth_map,
    show_loading_page=True,
    url="owid-choropleth",
)
PANDAS_PROFILING = Page(
    name="Pandas Profiling",
    source_code_url=GITHUB_PAGE_URL + "pandas_profiling_app/pandas_profiling_app.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "pandas_profiling_app.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
    ],
    component=pages.pandas_profiling_app,
    show_loading_page=False,
    url="pandas-profiling",
)
PARAM_REFERENCE_EXAMPLE = Page(
    name="Param Reference Example",
    source_code_url=GITHUB_PAGE_URL + "param_reference_example/param_reference_example.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "param_reference_example.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
    ],
    component=pages.param_reference_example,
    url="param-reference",
)
YAHOO_QUERY = Page(
    name="Yahoo Query",
    source_code_url=GITHUB_PAGE_URL + "yahooquery_app/yahooquery_app.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "yahooquery_app.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
    ],
    component=pages.yahooquery_app,
    show_loading_page=True,
    url="yahoo-query",
)
TEST_BOOTSTRAP_ALERTS = Page(
    name="Test Bootstrap Alerts",
    source_code_url=GITHUB_PAGE_URL + "awesome_panel_express_tests/test_bootstrap_alerts.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "test_bootstrap_alerts.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
        tags.AWESOMEPANEL_EXPRESS,
    ],
    component=pages.test_bootstrap_alerts,
    url="ext-alert",
)
TEST_BOOTSTRAP_CARD = Page(
    name="Test Bootstrap Card",
    source_code_url=GITHUB_PAGE_URL + "awesome_panel_express_tests/test_bootstrap_card.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "test_bootstrap_card.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
        tags.AWESOMEPANEL_EXPRESS,
    ],
    component=pages.test_bootstrap_card,
    show_loading_page=True,
    width=False,
    url="ext-card",
)
TEST_CODE = Page(
    name="Test Code",
    source_code_url=GITHUB_PAGE_URL + "awesome_panel_express_tests/test_code.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "test_code.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
        tags.AWESOMEPANEL_EXPRESS,
    ],
    component=pages.test_code,
    url="ext-code",
)
TEST_DATAFRAME = Page(
    name="Test DataFrame",
    source_code_url=GITHUB_PAGE_URL + "awesome_panel_express_tests/test_dataframe.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "test_dataframe.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
        tags.AWESOMEPANEL_EXPRESS,
    ],
    component=pages.test_dataframe,
    url="ext-dataframe",
)
TEST_ECHARTS = Page(
    name="Test ECharts",
    source_code_url=GITHUB_PAGE_URL + "awesome_panel_express_tests/test_echarts.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "test_echarts.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
        tags.AWESOMEPANEL_EXPRESS,
    ],
    component=pages.test_echarts,
    url="echarts",
)
TEST_MATERIAL = Page(
    name="Test Material Components",
    source_code_url=GITHUB_PAGE_URL + "awesome_panel_express_tests/test_material.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "test_material_components.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
    ],
    component=pages.test_material,
    url="ext-material",
)
TEST_MODEL_VIEWER = Page(
    name="Test Model Viewer",
    source_code_url=GITHUB_PAGE_URL + "awesome_panel_express_tests/test_model_viewer.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "test_model_viewer.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
    ],
    component=pages.test_model_viewer,
    url="ext-model-viewer",
)
TEST_PERSPECTIVE = Page(
    name="Test Perspective Viewer",
    source_code_url=GITHUB_PAGE_URL + "awesome_panel_express_tests/test_perspective.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "test_perspective.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
    ],
    component=pages.test_perspective,
    restrict_max_width=False,
    url="ext-perspective",
)
TEST_PROGRESS_EXTENSION = Page(
    name="Test Progress Extension",
    source_code_url=GITHUB_PAGE_URL + "awesome_panel_express_tests/test_progress_ext.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "test_progress_ext.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
        tags.AWESOMEPANEL_EXPRESS,
    ],
    component=pages.test_progress_ext,
    url="ext-progress",
)
TEST_SHARE_LINKS = Page(
    name="Test Social Links",
    source_code_url=GITHUB_PAGE_URL + "awesome_panel_express_tests/test_share_links.py",
    thumbnail_png_url=THUMBNAILS_ROOT + "test_share_links.png",
    tags=[
        tags.CODE,
        tags.APP_IN_GALLERY,
        tags.AWESOMEPANEL_EXPRESS,
    ],
    component=pages.test_share_links,
    url="ext-social-links",
)

PAGES = [
    HOME,
    ABOUT,
    BOOTSTRAP_DASHBOARD,
    CUSTOM_BOKEH_MODEL,
    DASHBOARD,
    DATA_EXPLORER,
    DETR,
    IMAGE_CLASSIFIER,
    JS_ACTIONS,
    KICKSTARTER_DASHBOARD,
    OWID_CHOROPLETH_MAP,
    PANDAS_PROFILING,
    PARAM_REFERENCE_EXAMPLE,
    YAHOO_QUERY,
    TEST_BOOTSTRAP_ALERTS,
    TEST_BOOTSTRAP_CARD,
    TEST_CODE,
    TEST_DATAFRAME,
    TEST_ECHARTS,
    TEST_MATERIAL,
    TEST_MODEL_VIEWER,
    TEST_PERSPECTIVE,
    TEST_PROGRESS_EXTENSION,
    TEST_SHARE_LINKS,
    ISSUES,
]

NON_GALLERY_PAGES = [
    HOME,
    ABOUT,
    ISSUES,
]

GALLERY_PAGES = [page for page in PAGES if page not in NON_GALLERY_PAGES]

URLS = {page.url: getattr(page.component, "view") for page in NON_GALLERY_PAGES + GALLERY_PAGES}
