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


def main():
    game_engine = engine.GameEngine()
    game_engine.spawn_asteroid()
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
        game_engine.draw_objects()
        game_engine.move_objects()
        game_engine.input_update()

        graphics.GraphicsEngine.reveal()
        #exit(0)

main()
