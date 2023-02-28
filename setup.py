from setuptools import find_packages, setup

setup(
    name="dataviz_dauphine_tunis",
    version="0.0.1",
    packages=find_packages(exclude=("tests", "tasks")),
    install_requires=[
        "google-cloud-bigquery==2.34.2",
        "google-cloud-secret-manager==2.9.2",
        "google-cloud-storage==2.2.1",
        "pandas==1.3.4",
        "pandas-gbq==0.15.0",
        "pyarrow>=3.0.0",
        "pytest>=6.2.3",
        "logzero",
        "scipy>=1.6.2",
        "pyyaml>=5.4.1",
        "flask==1.1.2",
        "param == 1.12.0",
        "holoviews == 1.14.2",
        "hvplot == 0.7.1",
        "lxml",
        "plotly",
        "folium",
        "invoke==1.3.0",
        "Pillow>=8.4.0",
        "panel==0.13.0",
        "bokeh==2.4.1",
        "redis",
        "numpy==1.21.3",
        "numerize==0.12",
        "colorcet==2.0.6",
        "matplotlib",
        "xlsxwriter",
        "pandasql",
        "aiohttp>=3.8.1",
        "requests>=2.26.0",
        "jinja2==2.11.3",
        "markupsafe==2.0.1",
        "webdriver-manager==3.8.3"

    ],
    url="",
    license="",
    author="Hadrien Mariaccia",
    author_email="",
    description="Data Viz Dauphine Tunis",
)
