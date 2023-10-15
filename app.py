import os
import panel as pn
import platform

# We need to configure the site before we import the pages
from TP4.config import site
from TP4 import pages
from TP4.constants.constants import ENV_LOCAL


# We need to import the application modules to get the applications added to the site

# To match the Cloud Run timeout value of 600s (10 mins)
ONE_SEC_MILLIS = 1000
UNUSED_SESSION_LIFETIME_MILLIS = 604800 * ONE_SEC_MILLIS
CHECK_UNUSED_SESSION_MILLIS = 30 * ONE_SEC_MILLIS

if __name__ == "__main__":
    address = os.getenv("BOKEH_ADDRESS", "0.0.0.0")
    env = os.getenv("ENV", ENV_LOCAL)
    port = 8000
    APP_ROUTES = {app.url: app.view for app in site.applications}
    # Create user settings table if doesn't exist
    if platform.system() == "Windows":
        pn.serve(APP_ROUTES, port=port, dev=False, address=address)
    else:
        pn.serve(
            APP_ROUTES, port=port, dev=False, show=False, address=address, websocket_origin=f"0.0.0.0:{port}",
            unused_session_lifetime_milliseconds=UNUSED_SESSION_LIFETIME_MILLIS,
            check_unused_sessions=CHECK_UNUSED_SESSION_MILLIS,
            autoreload=True,
            num_proc=5)
