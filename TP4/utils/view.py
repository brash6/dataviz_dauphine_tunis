import panel as pn
from logzero import logger

from TP4.constants.constants import ENV
from TP4.template import (
    FastDefaultTheme,
    LiverampDefaultTheme,
    LiverampTemplate,
    MaterialDefaultTheme,
    MaterialTemplate,
    VanillaDefaultTheme,
    VanillaTemplate,
)
from TP4.utils.notifications import (
    error_notification,
    success_notification,
    warning_notification,
)


def get_template(BQClient, Dashboard, name_tab="Sales Overview"):
    css = """
    h2 {
    color: #212121;
    font-family: 'Open Sans', sans-serif;
    font-weight: 500;
    font-size: 16pt;
    line-height: 1.5;
    }
    """
    pn.extension(raw_css=[css], notifications=True)
    """Returns the app in a Template"""
    pn.config.sizing_mode = "stretch_width"
    pn.config.notifications = True
    pn.state.notifications.position = 'top-left'
    logger.info("getting the tenant")
    tenant_id = 101015
    logger.info("getting the bqhandler")

    try:
        BQHandler = BQClient(tenant_id)

        # Modify the name and the title of the dashboard
        logger.info("getting the app")
        app = Dashboard(BQHandler, name="")
        logger.info("starting the layout")
        template = LiverampTemplate(title=name_tab,
                                    theme=LiverampDefaultTheme,
                                    header_background="#7ecb6f", font='Open Sans', accent_base_color="#56AA4E")
        template.main[:] = [app.main]
        template.sidebar[:] = [app.settings_panel]
        app._refresh_data()
        logger.info("finishing layout")
    except Exception as e:
        raise e
    return template

