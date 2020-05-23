import socket
from django.shortcuts import render
from plant_kiper import settings


def get_ip():
    """
    get ip of local machine
    source https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def home(request):
    ip = get_ip()
    return render(
        request,
        "home.html",
        {
            "version": settings.__version__,
            "ip": ip,
            "django_admin_url": f'http://{ip}:8001/admin',
            "api_gateway_url": f'http://{ip}:8001/api',
            "grafana_url": f'http://{ip}:3000/',
        }
    )
