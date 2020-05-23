import requests
from requests.exceptions import ConnectionError


def is_api_gateway_up(host="http://api-gateway:8001/admin") -> bool:
    """
    true if api gateway is ready,
    mean django make migrations + migrate is done
    controller can access to ORM
    :param host:
    :return:
    """
    try:
        if requests.get(host).ok:
            return True
        else:
            return False
    except ConnectionError:
        return False
