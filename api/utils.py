import os
import json
import urllib

from PIL import Image
from pathlib import Path
from django.core.mail import send_mail
from django.conf import settings
from math import sin, cos, sqrt, atan2, radians

R = 6373.0
BASE_DIR = Path(__file__).resolve().parent.parent
MAX_THUMBNAIL_SIZE = 900
PRIVATE_IPS_PREFIX = ('10.', '172.', '192.',)


def add_watermark(self):
    image = Image.open(self.avatar.path)
    watermark = Image.open(os.path.join(BASE_DIR, 'static/img/watermark.png'))
    width = self.avatar.width
    height = self.avatar.height
    max_size = max(width, height)
    image = image.resize(
        (round(width / max_size * MAX_THUMBNAIL_SIZE),
         round(height / max_size * MAX_THUMBNAIL_SIZE)),
        Image.ANTIALIAS
    )
    image.paste(watermark, (30, 1), mask=watermark)
    image.save(self.avatar.path)


def match(user, user_to):
    result = ""
    for like in user.got_like.all():
        if like.user_to == user and like.user != like.user_to:
            result += f"У вас взаимная симпатия c {user_to.f_name}! Email участника: {user_to.email}"
            subject = f" У вас взаимная симпатия с "
            body = f"Поздравляем!\n email участника: "
            send_mail(
                f"{subject} {user_to.f_name}",
                f"{body} {user_to.email}",
                settings.EMAIL_HOST_USER, [user.email],
                fail_silently=False
            )
            send_mail(
                f"{subject} {user.f_name}",
                f"{body} {user.email}",
                settings.EMAIL_HOST_USER, [user_to.email],
                fail_silently=False
            )
            break
    return result


def get_client_ip(request):
    remote_address = request.META.get('REMOTE_ADDR')
    ip = remote_address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        while (len(proxies) > 0 and
               proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
        if len(proxies) > 0:
            ip = proxies[0]
    return ip


def get_res(request):
    client_ip = get_client_ip(request)
    if client_ip is None:
        client_ip = "0.0.0.0"
    ip_address = '106.220.90.88'
    try:
        url = 'http://api.ipfind.com/?ip=' + client_ip
        response = urllib.request.urlopen(url)
        data1 = json.loads(response.read())
        longitude = data1["longitude"]
        latitude = data1["latitude"]
    except:
        url = 'http://api.ipfind.com/?ip=' + ip_address
        response = urllib.request.urlopen(url)
        data1 = json.loads(response.read())
        longitude = data1["longitude"]
        latitude = data1["latitude"]
    return [longitude, latitude]


def get_distance(lon1, lat1, lon2, lat2):
    lon1 = radians(lon1)
    lat1 = radians(lat1)
    lon2 = radians(lon2)
    lat2 = radians(lat2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    #km
    distance = R * c

    return distance
