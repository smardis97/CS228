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
        self.clock_margin = 0.
        self.last_clock_update = time.time()
        self.last_snow_update = time.time()
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
        if time.time() - self.last_snow_update > constants.STAR_GENERATION_TIME:
            self.spawn_stars()
            self.last_snow_update = time.time()
        self.clock_update()
        self.draw_objects()
        self.move_objects()
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
        pass

    def move_objects(self):
        self.player.update()
        for obj in self.game_objects:
            obj.update(self.player.velocity)
        for obj in self.background_objects:
            obj.update(self.player.velocity)
        self.check_collisions()

    def spawn_asteroid(self):
        self.game_objects.append(game_object.Asteroid((0, 0), (0, 0), 3))

    def directional_asteroid_position(self):
        player_direction = utility.cartesian_to_polar(self.player.get_velocity())[0]
        point_a = utility.polar_to_cartesian((player_direction - constants.ASTEROID_SPAWN_BREDTH / 2,
                                              constants.ASTEROID_SPAWN_RANGE))
        point_b = utility.polar_to_cartesian((player_direction + constants.ASTEROID_SPAWN_BREDTH / 2,
                                              constants.ASTEROID_SPAWN_RANGE))
        min_spawn_x = min([point_a[0], point_b[0]])
        max_spawn_x = max([point_a[0], point_b[0]])
        min_spawn_y = min([point_a[1], point_b[1]])
        max_spawn_y = max([point_a[1], point_b[1]])
        spawn_x = random.randint(min_spawn_x, max_spawn_x)
        spawn_y = random.randint(min_spawn_y, max_spawn_y)
        return spawn_x, spawn_y

    def herd_asteroids(self):
        pass

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
        stars_count = constants.STAR_GENERATION_SPAN / constants.STAR_SEPARATION
        for i in range(stars_count):
            self.background_objects.append(graphics.Circle(self.star_position(i),
                                                           random.randint(constants.STAR_MIN_RADIUS,
                                                                          constants.STAR_MAX_RADIUS)))

    @staticmethod
    def star_position(i):
        x_val = - (constants.STAR_GENERATION_SPAN / 2) + (constants.STAR_SEPARATION * i) +\
                random.randint(- math.floor(constants.STAR_SEPARATION * 0.2), math.ceil(constants.STAR_SEPARATION * 0.2))
        y_val = constants.STAR_MIN_HEIGHT + random.randint(- constants.STAR_HEIGHT_VARIATION, constants.STAR_HEIGHT_VARIATION)

        return x_val, y_val

    def clock_update(self):
        last_update = self.last_clock_update
        self.last_clock_update = time.time()
        self.clock_margin = (self.last_clock_update - last_update) * 1000
        print self.clock_margin
