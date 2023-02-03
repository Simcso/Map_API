import sys
import pygame
from load_map import Map, view_map


clock = pygame.time.Clock()
screen = pygame.display.set_mode()
map = Map((47.8908, 56.6388))
view_map(screen)
while True:
    for event in pygame.event.get():
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

