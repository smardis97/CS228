import constants
import utility
import graphics
import game_object
import settable
import pygame
import random
import time
import math


class GameEngine:
    def __init__(self):
        self.game_objects = []
        self.background_objects = []
        self.player = game_object.Player()
        self.window = graphics.GraphicsEngine()
        self.game_state = constants.GAME_PLAY
        # self.mouse = {
        #     'button1'
        # }
        self.min_coords = {'x': 1000, 'y': 1000, 'z': 1000}
        self.max_coords = {'x': -1000, 'y': -1000, 'z': -1000}
        self.key_status = {
            ord('a'): False,
            ord('b'): False,
            ord('c'): False,
            ord('d'): False,
            ord('e'): False,
            ord('f'): False,
            ord('g'): False,
            ord('h'): False,
            ord('i'): False,
            ord('j'): False,
            ord('k'): False,
            ord('l'): False,
            ord('m'): False,
            ord('n'): False,
            ord('o'): False,
            ord('p'): False,
            ord('q'): False,
            ord('r'): False,
            ord('s'): False,
            ord('t'): False,
            ord('u'): False,
            ord('v'): False,
            ord('w'): False,
            ord('x'): False,
            ord('y'): False,
            ord('z'): False,
            304: False
        }

    def update_game(self):
        self.draw_objects()
        self.move_objects()
        self.check_collisions()
        self.input_update()

    def key_listener(self, event):
        if event.type == pygame.KEYDOWN:
            if ord('a') <= event.__dict__["key"] <= ord('z'):
                self.key_status[event.__dict__["key"]] = True
            elif event.__dict__["key"] == 304:
                self.key_status[event.__dict__["key"]] = True

        elif event.type == pygame.KEYUP:
            if 97 <= event.__dict__["key"] <= 122:
                self.key_status[event.__dict__["key"]] = False
            elif event.__dict__["key"] == 304:
                self.key_status[event.__dict__["key"]] = False

    def update_mouse_pos(self, event):
        pass

    def mouse_listener(self, event):
        pass

    def draw_objects(self):
        self.window.clear()
        self.player.draw_self_to_layer(self.window, 5)
        for obj in self.game_objects:
            obj.draw_self_to_layer(self.window, 4)
        for obj in self.background_objects:
            obj.draw_self_to_layer(self.window, 1)
        self.window.draw()

    def check_collisions(self):
        for asteroid_1 in self.game_objects:
            for asteroid_2 in self.game_objects[self.game_objects.index(asteroid_1)+1:]:
                if asteroid_1.test_collide(asteroid_2):
                    game_object.Asteroid.collide_asteroid(asteroid_1, asteroid_2)

    def move_objects(self):
        self.player.update()
        for obj in self.game_objects:
            obj.update()
        self.check_collisions()

    def spawn_asteroid(self):
        self.game_objects.append(game_object.Asteroid(GameEngine.asteroid_position(),
                                                      utility.polar_to_cartesian(GameEngine.random_velocity()),
                                                      random.randint(- constants.ASTEROID_MAX_ANG_VEL,
                                                                     constants.ASTEROID_MAX_ANG_VEL)))

    @staticmethod
    def random_velocity():
        heading = random.randint(0, 360)
        magnitude = random.randint(1, constants.ASTEROID_MAX_VEL)
        return heading, magnitude

    @staticmethod
    def asteroid_position():
        x_pos = random.randint(- constants.ASTEROID_MAX_RADIUS, constants.ASTEROID_MAX_RADIUS)
        y_pos = random.randint(- constants.ASTEROID_MAX_RADIUS, constants.ASTEROID_MAX_RADIUS)
        return x_pos, y_pos

    def collect_garbage(self):
        pass

    def input_update(self):
        if self.key_status[ord('a')]:
            self.player.turn('left')
        if self.key_status[ord('d')]:
            self.player.turn('right')
        if self.key_status[ord('w')]:
            self.player.thrust()
        if self.key_status[304]:
            self.player.brake()

    def spawn_stars(self):
        for i in range(constants.STAR_COUNT):
            self.background_objects.append(game_object.Snow((random.randint(0, constants.GAME_ARENA_DIMENSIONS[0]),
                                                             random.randint(0, constants.GAME_ARENA_DIMENSIONS[1]))))
