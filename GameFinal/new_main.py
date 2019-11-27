import sys

sys.path.insert(0, '..')

import Leap
import graphics
import constants
import game_object
import engine
import numpy as np
import dict
import pygame
import utility
import time


def main():
    game_engine = engine.GameEngine()
    for i in range(4):
        game_engine.spawn_asteroid()
    game_engine.spawn_stars()
    #
    #
    #  MAIN GAME LOOP
    #
    #
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            else:
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    game_engine.key_listener(event)
                elif event.type == pygame.MOUSEMOTION:
                    game_engine.update_mouse_pos(event)
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    game_engine.mouse_listener(event)
        graphics.GraphicsEngine.prepare(game_engine.window)

        # main runtime body
        game_engine.update_game()

        graphics.GraphicsEngine.reveal()

main()
