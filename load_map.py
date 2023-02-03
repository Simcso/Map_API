from PIL import Image
from io import BytesIO
import requests
import pygame


proxyDict = {"http": 'http://s2021010055:lazur2097584+@proxy.volgatech.net:3128',
                 "https": 'http://s2021010055:lazur2097584+@proxy.volgatech.net:3128'}
map_api_server = "http://static-maps.yandex.ru/1.x/"


class Map:
    def __init__(self, adress, delta='0.05', type='map', name='map.png'):
        self.adress, self.delta, self.type, self.name = adress, delta, type, name
        map_params = {"ll": f"{adress[0]},{adress[1]}", "spn": f"{delta},{delta}", "l": type}
        Image.open(BytesIO(requests.get(map_api_server, params=map_params, proxies=proxyDict).content)).save(name)

    def change_delta(self, step):
        try:
            self.__init__(self.adress, str(eval(self.delta + step + str(float(self.delta) / 1.4))),
                          self.type, self.name)
        except Exception:
            pass


def view_map(screen):
    screen.fill('gray')
    screen.blit(pygame.transform.scale(pygame.image.load('map.png'),
                                       (screen.get_width() - 400, screen.get_height() - 100)), (350, 50))