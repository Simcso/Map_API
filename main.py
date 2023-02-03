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
            map.change_delta(0.1 if event.scancode == 78 else -0.1)
            view_map(screen)
        elif event.type == pygame.KEYDOWN and event.scancode == 41:
            # Завершаем программу
            pygame.quit()
            sys.exit()
    pygame.display.flip()
    clock.tick(60)

