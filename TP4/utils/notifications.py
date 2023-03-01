import panel as pn


def info_notification(text, duration=10000):
    pn.state.notifications.info(text, duration=duration)
    return


def warning_notification(text, duration=10000):
    pn.state.notifications.warning(text, duration=duration)
    return


def error_notification(text, duration=10000):
    pn.state.notifications.error(text, duration=duration)
    return


def success_notification(text, duration=10000):
    pn.state.notifications.success(text, duration=duration)
    return
