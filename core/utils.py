from datetime import datetime


def get_now():
    return datetime.isoformat(datetime.utcnow())


def get_timezone_now(_timezone: str):
    """

    :param _timezone:
    :return:
    """
    return "pass"
