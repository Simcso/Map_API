import sys
import pygame
from load_map import load_map

load_map((47.8908, 56.6388))

screen = pygame.display.set_mode()
screen.fill('gray')
screen.blit(pygame.transform.scale(pygame.image.load('map.png'),
                                   (screen.get_width() - 400, screen.get_height() - 100)), (350, 50))
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.scancode == 41:
            # Завершаем программу
            pygame.quit()
            sys.exit()
    pygame.display.flip()
