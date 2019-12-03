import sys

sys.path.insert(0, '..')

import Leap
import constants
import utility
import graphics
import game_object
import settable
import pygame
import random
import numpy as np
import time
import math
import pickle
import dict


class GameEngine:
    def __init__(self):
        dict.start_up()
        self.game_objects = []
        self.background_objects = []
        self.player = game_object.Player()
        self.current_user = None
        self.window = graphics.GraphicsEngine()
        self.gui = graphics.GUI(self.window, self)
        self.game_state = constants.GAME_MENU
        self.controller = Leap.Controller()
        self.game_start = time.time()
        self.save_number = 0
        self.previous_number = -1
        self.current_number = -1
        self.correct_count = constants.CORRECT_COUNT
        self.classifier = pickle.load(open("{}{}".format(constants.DATA_PATH, constants.NN_CLASSIFIER_FILE)))
        self.test_data = np.zeros((1, 30), dtype='f')
        self.next_bone_index = 0
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
        self.choose_next_number()
        self.spawn_stars()

    def attempt_increment(self):
        if self.current_user is not None:
            dict.database[self.current_user][constants.ATTEMPTS_KEY[self.current_number]] += 1

    def success_increment(self):
        if self.current_user is not None:
            dict.database[self.current_user][constants.SUCCESSES_KEY[self.current_number]] += 1

    def switch_users(self, new_user):
        dict.save()
        self.current_user = dict.login(new_user)

    def initialize_game(self):
        for key in self.key_status:
            self.key_status[key] = False
        del self.game_objects[:]
        self.game_objects = []
        self.player.set_velocity(0, 0)
        self.player.angular_velocity = 0
        self.player.heading = 0
        self.player.reset_position()
        self.game_start = time.time()
        self.game_state = constants.GAME_PLAY
        self.gui.menu_state = constants.MENU_NONE

    def game_level(self):
        return int(math.floor(self.elapsed_time() / 15))

    def elapsed_time(self):
        elapsed = time.time() - self.game_start
        return elapsed

    def update_game(self):
        game_level = self.game_level()
        if self.count_asteroids() < game_level + 3:
            for i in range(game_level + 3 - self.count_asteroids()):
                self.spawn_asteroid()
        frame = self.controller.frame()
        if len(frame.hands) > 0:
            self.next_bone_index = 0
            self.handle_frame(frame)
            self.test_network()
        self.gui.update(self.current_number,
                        dict.database[self.current_user][constants.SUCCESSES_KEY[self.current_number]]
                        if self.current_user is not None else 0)
        self.draw_objects()
        self.gui.draw_gui()
        self.move_objects()
        self.check_collisions()
        self.input_update()

    def handle_frame(self, frame):
        hand = frame.hands[0]
        fingers = hand.fingers
        for finger in fingers:
            self.handle_finger(finger)

    def handle_finger(self, finger):
        for b in range(4):
            self.handle_bone(finger.bone(b), b)

    def handle_bone(self, bone, bone_type):
        base = bone.prev_joint
        base = graphics.GUI.leap_to_window(base)
        tip = bone.next_joint
        if bone_type == 0 or bone_type == 3:
            self.test_data[0, self.next_bone_index] = bone.next_joint[0]
            self.test_data[0, self.next_bone_index + 1] = bone.next_joint[1]
            self.test_data[0, self.next_bone_index + 2] = bone.next_joint[2]
            self.next_bone_index = self.next_bone_index + 3
        tip = graphics.GUI.leap_to_window(tip)
        self.gui.draw_bone(base, tip, bone_type)

    def choose_next_number(self):
        while self.current_number == self.previous_number:
            self.current_number = random.randint(0, 9)
        self.attempt_increment()

    def test_network(self):
        if self.game_state == constants.GAME_PLAY:
            self.test_data = utility.center_data(self.test_data)
            if self.current_number == self.classifier.Predict(self.test_data):
                self.correct_count -= 1
                if self.correct_count == 0:
                    self.success_increment()
                    self.previous_number = self.current_number
                    self.choose_next_number()
                    self.add_bullet()
                    self.correct_count = constants.CORRECT_COUNT

    def key_listener(self, event):
        if self.game_state == constants.GAME_PLAY:
            if event.type == pygame.KEYDOWN:
                if ord('a') <= event.__dict__["key"] <= ord('z'):
                    self.key_status[event.__dict__["key"]] = True
                elif event.__dict__["key"] == 304:
                    self.key_status[event.__dict__["key"]] = True
                elif event.__dict__["key"] == 27:
                    exit(0)
            elif event.type == pygame.KEYUP:
                if 97 <= event.__dict__["key"] <= 122:
                    self.key_status[event.__dict__["key"]] = False
                elif event.__dict__["key"] == 304:
                    self.key_status[event.__dict__["key"]] = False
                elif event.__dict__["key"] == 32:
                    self.save_hand()
        elif self.game_state == constants.GAME_MENU:
            self.gui.key_listener(event)

    def save_hand(self):
        frame = self.controller.frame()
        if len(frame.hands) > 0:
            gesture_data = np.zeros((5, 4, 2, 3), dtype='f')
            for f in range(5):
                for b in range(4):
                    bone = frame.hands[0].fingers[f].bone(b)
                    gesture_data[f][b][0][0] = bone.prev_joint[0]
                    gesture_data[f][b][0][1] = bone.prev_joint[1]
                    gesture_data[f][b][0][2] = bone.prev_joint[2]
                    gesture_data[f][b][1][0] = bone.next_joint[0]
                    gesture_data[f][b][1][1] = bone.next_joint[1]
                    gesture_data[f][b][1][2] = bone.next_joint[2]
            pickle_out = open("{}{}".format(constants.DATA_PATH, "example_{}.dat".format(self.save_number % 10)), "wb")
            pickle.dump(gesture_data, pickle_out)
            print "SAVED"
            pickle_out.close()
            self.save_number += 1

    def mouse_listener(self, event):
        if self.game_state == constants.GAME_MENU:
            if event.type == pygame.MOUSEMOTION:
                self.gui.mouse_update(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.gui.mouse_click(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                pass

    def add_bullet(self):
        self.game_objects.append(game_object.Bullet(self.player.heading, self.player.position))

    def draw_objects(self):
        self.player.draw_self_to_layer(self.window, 5)
        for obj in self.game_objects:
            obj.draw_self_to_layer(self.window, 4)
        for obj in self.background_objects:
            obj.draw_self_to_layer(self.window, 1)
        self.window.draw()
        self.window.clear()

    def count_asteroids(self):
        count = 0
        for obj in self.game_objects:
            if type(obj) == game_object.Asteroid:
                count += 1
        return count

    def check_collisions(self):
        for object_1 in self.game_objects:
            if object_1.test_collide(self.player) and self.game_state == constants.GAME_PLAY:
                self.game_state = constants.GAME_MENU
                self.gui.state_change(constants.MENU_OVER)
            for object_2 in self.game_objects[self.game_objects.index(object_1)+1:]:
                if object_1.test_collide(object_2):
                    if type(object_1) == game_object.Bullet:
                        del object_2
                    else:
                        pass
                        #game_object.Asteroid.collide_asteroid(asteroid_1, asteroid_2)

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
        magnitude = random.randint(constants.ASTEROID_MIN_VEL, constants.ASTEROID_MAX_VEL)
        return heading, magnitude

    @staticmethod
    def asteroid_position():
        x_pos = random.randint(- constants.ASTEROID_MAX_RADIUS, constants.ASTEROID_MAX_RADIUS)
        y_pos = random.randint(- constants.ASTEROID_MAX_RADIUS, constants.ASTEROID_MAX_RADIUS)
        return x_pos, y_pos

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
