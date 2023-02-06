import sys
import pygame
from load_map import *


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode()

cords = find_toponym('Йошкар-Ола')
map = Map(cords, cords)
view_map(screen)

text = TextInput(screen, 20, 30, 265, 30, 'Введите запрос', 20)
but = Button(screen, 290, 30, 50, 30, 'DEL', 20)
while True:
    text.update()
    if but.update(map):
        map = but.update(map)
    for event in pygame.event.get():
        if text.text_input:
            if event.type == pygame.TEXTINPUT:
                text.text += event.text
            elif event.type == pygame.KEYDOWN and event.scancode == 42:
                text.text = text.text[:-1]
            elif event.type == pygame.KEYDOWN and event.scancode == 40:
                text.text_input = False
                cords = find_toponym(text.get_text())
                if cords:
                    map = Map(cords, cords, map.delta, map.type, map.name)
                    view_map(screen)
        else:
            if event.type == pygame.KEYDOWN and event.scancode in [78, 75]:
                map.change_delta('+' if event.scancode == 78 else '-')
                view_map(screen)
            elif event.type == pygame.KEYDOWN and event.scancode in [79, 80, 81, 82]:
                map.change_cords((0 if event.scancode not in [79, 80] else {79: '+', 80: '-'}[event.scancode],
                                  0 if event.scancode not in [81, 82] else {82: '+', 81: '-'}[event.scancode]))
                view_map(screen)
            elif event.type == pygame.KEYDOWN and event.scancode == 41:
                # Завершаем программу
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.scancode in [30, 31, 32]:
                map.change_type(event.scancode)
                view_map(screen)
    pygame.display.flip()
    clock.tick(60)

