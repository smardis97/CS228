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


class GameEngine:
    def __init__(self):
        self.game_objects = []
        self.background_objects = []
        self.player = game_object.Player()
        self.window = graphics.GraphicsEngine()
        self.gui = graphics.GUI(self.window)
        self.game_state = constants.GAME_PLAY
        self.controller = Leap.Controller()
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

    def update_game(self):
        frame = self.controller.frame()
        if len(frame.hands) > 0:
            self.next_bone_index = 0
            self.handle_frame(frame)
            self.test_network()
        self.gui.update(self.current_number, 0)
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

    def test_network(self):
        self.test_data = utility.center_data(self.test_data)
        if self.current_number == self.classifier.Predict(self.test_data):
            self.correct_count -= 1
            if self.correct_count == 0:
                self.previous_number = self.current_number
                self.choose_next_number()
                # TODO: Fire Bullet
                self.correct_count = constants.CORRECT_COUNT

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
            elif event.__dict__["key"] == 32:
                self.save_hand()

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
            pickle_out = open("{}{}".format(constants.DATA_PATH, "example_9.dat"), "wb")
            pickle.dump(gesture_data, pickle_out)
            print "SAVED"
            pickle_out.close()

    def update_mouse_pos(self, event):
        pass

    def mouse_listener(self, event):
        pass

    def draw_objects(self):
        self.player.draw_self_to_layer(self.window, 5)
        for obj in self.game_objects:
            obj.draw_self_to_layer(self.window, 4)
        for obj in self.background_objects:
            obj.draw_self_to_layer(self.window, 1)
        self.window.draw()
        self.window.clear()

    def check_collisions(self):
        for asteroid_1 in self.game_objects:
            for asteroid_2 in self.game_objects[self.game_objects.index(asteroid_1)+1:]:
                if asteroid_1.test_collide(asteroid_2):
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
