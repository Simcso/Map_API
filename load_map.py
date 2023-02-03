from PIL import Image
from io import BytesIO
import requests


def load_map(adress, delta='0.05', type='map', name='map.png'):
    proxyDict = {"http": 'http://s2021010055:lazur2097584+@proxy.volgatech.net:3128',
                 "https": 'http://s2021010055:lazur2097584+@proxy.volgatech.net:3128'}
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_params = {"ll": f"{adress[0]},{adress[1]}", "spn": f"{delta},{delta}", "l": type}
    Image.open(BytesIO(requests.get(map_api_server, params=map_params, proxies=proxyDict).content)).save(name)
