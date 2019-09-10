import script
import threading
from sprites import Sprite
import os

import pygame

interface = script.spritesetup()
thread = threading.Thread(target=script.runscript, args=(interface,))
thread.start()

pygame.init()
screen = pygame.display.set_mode((858,480))
running = True
clock = pygame.time.Clock()

pygame.display.set_caption('Rina')
pygame.display.set_icon(pygame.image.load("assets/favicon.png").convert_alpha())

pygame.mixer.music.load('assets/rinabgmusic.mp3')
pygame.mixer.music.play(-1)

while running:

    sprites = Sprite.getinstances()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os._exit(0)
        for sprite in sprites:
            sprite.event_update(event)
        
    # Continuous updates
    for sprite in sprites:
        sprite.continuous_update()

    # Rendering
    screen.fill((255, 255, 255))
    spritescopy = sprites.copy()
    for sprite in spritescopy:
        sprite.render(screen)

    pygame.display.update()
    clock.tick(60)