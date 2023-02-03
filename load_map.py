from PIL import Image
from io import BytesIO
import requests
import pygame


proxyDict = {"http": 'http://s2021010055:lazur2097584+@proxy.volgatech.net:3128',
                 "https": 'http://s2021010055:lazur2097584+@proxy.volgatech.net:3128'}
map_api_server = "http://static-maps.yandex.ru/1.x/"
map_types = {30: 'map', 31: 'sat', 32: 'sat,skl'}


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

    def change_cords(self, cords):
        try:
            self.__init__((self.adress[0] + float(cords[0] + str(float(self.delta) / 2)) if cords[0] else self.adress[0],
                           self.adress[1] + float(cords[1] + str(float(self.delta) / 2)) if cords[1] else self.adress[1]),
                          self.delta, self.type, self.name)
        except Exception:
            pass

    def change_type(self, map_type):
        try:
            self.__init__(self.adress, self.delta, map_types[map_type], self.name)
        except Exception:
            pass


def view_map(screen):
    screen.fill('gray')
    screen.blit(pygame.transform.scale(pygame.image.load('map.png'),
                                       (screen.get_width() - 400, screen.get_height() - 100)), (350, 50))