from PIL import Image
from io import BytesIO
import requests
import pygame


map_api_server = "http://static-maps.yandex.ru/1.x/"
map_types = {30: 'map', 31: 'sat', 32: 'sat,skl'}


class TextInput:
    def __init__(self, screen, x, y, width, height, text, font_size=40, font_name='Arial'):
        self.screen, self.x, self.y, self.width, self.height, self.text = screen, x, y, width, height, text
        self.text_input, self.font_name, self.font_size = False, font_name, font_size
        self.Surface = pygame.Surface((self.width, self.height))
        self.Surface.fill('black')
        rect = pygame.Surface((self.width - 4, self.height - 4))
        rect.fill('white')
        self.Surface.blit(rect, (2, 2))
        self.Rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # Создаём шрифт нужно цвета
        self.Text = pygame.font.SysFont(self.font_name, self.font_size).render(self.text, True, 'grey')
        # Добавляем текст на поверхность
        self.Surface.blit(self.Text, [self.Rect.width / 2 - self.Text.get_rect().width / 2,
                                      self.Rect.height / 2 - self.Text.get_rect().height / 2])
        # Накладываем поверхность поверх экрана
        self.screen.blit(self.Surface, self.Rect)

    def get_text(self):
        result = self.text
        self.__init__(self.screen, self.x, self.y, self.width, self.height, self.text, self.font_size, self.font_name)
        return result

    def update(self):
        self.Surface = pygame.Surface((self.width, self.height))
        self.Surface.fill('black')
        rect = pygame.Surface((self.width - 4, self.height - 4))
        rect.fill('white')
        self.Surface.blit(rect, (2, 2))
        # Создаём шрифт нужно цвета
        self.Text = pygame.font.SysFont(self.font_name, self.font_size). \
            render(self.text, True, 'black' if self.text_input else 'gray')
        # Проверяем находиться ли курсор на кнопке
        if self.Rect.collidepoint(pygame.mouse.get_pos()):
            # Создаём шрифт нужно цвета
            self.Text = pygame.font.SysFont(self.font_name, self.font_size). \
                render(self.text, True, '#666666')
            # Проверяем нажата ли кнопка
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.text_input, self.text = True, ''
        # Добавляем текст на поверхность
        self.Surface.blit(self.Text, [self.Rect.width / 2 - self.Text.get_rect().width / 2,
                                      self.Rect.height / 2 - self.Text.get_rect().height / 2])
        # Накладываем поверхность поверх экрана
        self.screen.blit(self.Surface, self.Rect)


class Button:
    def __init__(self, screen, x, y, width, height, text, font_size=40, font_name='Arial'):
        self.screen, self.x, self.y, self.width, self.height, self.text = screen, x, y, width, height, text
        self.text_input, self.font_name, self.font_size = False, font_name, font_size
        self.Surface = pygame.Surface((self.width, self.height))
        self.Surface.fill('black')
        rect = pygame.Surface((self.width - 4, self.height - 4))
        rect.fill('white')
        self.Surface.blit(rect, (2, 2))
        self.Rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # Создаём шрифт нужно цвета
        self.Text = pygame.font.SysFont(self.font_name, self.font_size).render(self.text, True, 'grey')
        # Добавляем текст на поверхность
        self.Surface.blit(self.Text, [self.Rect.width / 2 - self.Text.get_rect().width / 2,
                                      self.Rect.height / 2 - self.Text.get_rect().height / 2])
        # Накладываем поверхность поверх экрана
        self.screen.blit(self.Surface, self.Rect)

    def update(self, map):
        self.Surface = pygame.Surface((self.width, self.height))
        self.Surface.fill('black')
        rect = pygame.Surface((self.width - 4, self.height - 4))
        rect.fill('white')
        self.Surface.blit(rect, (2, 2))
        # Создаём шрифт нужно цвета
        self.Text = pygame.font.SysFont(self.font_name, self.font_size). \
            render(self.text, True, 'black' if self.text_input else 'gray')
        # Проверяем находиться ли курсор на кнопке
        if self.Rect.collidepoint(pygame.mouse.get_pos()):
            # Создаём шрифт нужно цвета
            self.Text = pygame.font.SysFont(self.font_name, self.font_size). \
                render(self.text, True, '#666666')
            # Проверяем нажата ли кнопка
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                cords = find_toponym('Йошкар-Ола')
                map = Map(cords, cords)
                view_map(self.screen)
                return map
        # Добавляем текст на поверхность
        self.Surface.blit(self.Text, [self.Rect.width / 2 - self.Text.get_rect().width / 2,
                                      self.Rect.height / 2 - self.Text.get_rect().height / 2])
        # Накладываем поверхность поверх экрана
        self.screen.blit(self.Surface, self.Rect)


class Map:
    def __init__(self, cords, point=None, delta='0.05', type='map', name='map.png'):
        self.cords, self.point, self.delta, self.type, self.name = cords, point, delta, type, name
        map_params = {'ll': f'{cords[0]},{cords[1]}', 'spn': f'{delta},{delta}', 'l': type}
        if self.point:
            map_params['pt'] = f'{point[0]},{point[1]},pm2dgl'
        Image.open(BytesIO(requests.get(map_api_server, params=map_params).content)).save(name)

    def change_delta(self, step):
        try:
            self.__init__(self.cords, self.point, str(eval(self.delta + step + str(float(self.delta) / 1.4))),
                          self.type, self.name)
        except Exception:
            pass

    def change_cords(self, cords):
        try:
            self.__init__(
                (float(self.cords[0]) + float(cords[0] + str(float(self.delta) / 2)) if cords[0] else self.cords[0],
                 float(self.cords[1]) + float(cords[1] + str(float(self.delta) / 2)) if cords[1] else self.cords[1]),
                self.point, self.delta, self.type, self.name)
        except Exception:
            pass

    def change_type(self, map_type):
        self.__init__(self.cords, self.point, self.delta, map_types[map_type], self.name)


def view_map(screen):
    screen.fill('gray')
    screen.blit(pygame.transform.scale(pygame.image.load('map.png'),
                                       (screen.get_width() - 400, screen.get_height() - 100)), (350, 50))


def find_toponym(toponym):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {"apikey": "40d1649f-0493-4b70-98ba-98533de7710b", "geocode": toponym, "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        return None  # обработка ошибочной ситуации
    # Преобразуем ответ в json-объект
    json_response = response.json()
    if json_response["response"]['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found'] == '0':
        return None  # обработка ошибочной ситуации
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_cords = toponym["Point"]["pos"]
    # Долгота и широта:
    return toponym_cords.split(" ")