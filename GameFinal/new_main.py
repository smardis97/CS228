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
    #
    #
    #  MAIN GAME LOOP
    #
    #
    while True:
        for event in pygame.event.get():
            #print event
            if event.type == pygame.QUIT:
                exit(0)
            else:
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    game_engine.key_listener(event)
                elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    game_engine.mouse_listener(event)
        graphics.GraphicsEngine.prepare(game_engine.window)

        # main runtime body
        game_engine.update_game()

        graphics.GraphicsEngine.reveal()

main()
