# Built-in Imports
import sys
sys.path.insert(0, '..')
import random
import numpy as np
import time
import math
import pickle

# Third-party Imports
import pygame
import Leap

# Local Imports
from constants import *
from game_object import *
from graphics import *
import utility
import dict
import settable


class GameEngine:
    """
    This is the class that handles the majority of abstract game logic that is not performed by a specific object.

    Attributes:
        window              (GraphicsEngine):   The main game window, handles drawing the game objects to the screen.
        gui                 (GUI):              Controls and displays the menus, handles key and mouse input from user.
        game_objects        (list<GameObject>): Contains all interactable game objects, excluding the player.
        background_objects  (list<GameObject>): Contains all the background stars.
        player              (Player):           The Player object, controls the behavior of the player avatar.
        current_user        (String):           The string name of the current user profile.
        game_state          (String):           String representing the current state of the game. Presets in constants.
        game_start          (Float):            System time in seconds when the current game began.
        save_number         (int):              Number representing the name of the next example to be saved.
        previous_number     (int):              Int representing the last number that the user signed correctly.
        current_number      (int):              Int representing the number currently being presented to the user.
        correct_count       (int):              Countdown value, number of cycles the user needs to correctly sign for.
        key_status          (dict):             Dict tracking what keys are being held down.
        controller          (Controller):       Provides motion data from Leap Motion Device.
        test_data           (ndarray):          Array of coordinates of the hand in view, tested against KNN Network.
        classifier          (ndarray):          Array representing the training and test data of KNN Network.
        next_bone_index     (int):              Int representing the index of the next bone to be added to test_data.
    """
    def __init__(self):
        dict.start_up()  # Loads saved profile data into dict.database
        #
        # MAIN GAME OBJECTS -------------------------------------------------------------------------- MAIN GAME OBJECTS
        #
        self.window = graphics.GraphicsEngine()
        self.gui = graphics.GUI(self.window, self)
        self.game_objects = []
        self.background_objects = []
        self.player = Player()
        #
        # GAME LOGIC VARIABLES -------------------------------------------------------------------- GAME LOGIC VARIABLES
        #
        self.current_user = None
        self.game_state = GAME_MENU
        self.game_start = time.time()
        self.save_number = 0
        self.previous_number = -1
        self.current_number = -1
        self.correct_count = CORRECT_COUNT
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
        #
        # NN OBJECTS AND VARIABLES ------------------------------------------------------------ NN OBJECTS AND VARIABLES
        #
        self.controller = Leap.Controller()
        self.test_data = np.zeros((1, 30), dtype='f')
        self.classifier = pickle.load(open("{}{}".format(DATA_PATH, NN_CLASSIFIER_FILE)))
        self.next_bone_index = 0

        # Called to setup basic functionality

        self.choose_next_number()
        self.spawn_stars()

    ####################################################################################################################
    # HIGH LEVEL GAME LOGIC ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ HIGH LEVEL GAME LOGIC #
    ####################################################################################################################

    def initialize_game(self):
        """
        Resets all game relevant fields and then starts the new game.

        Resets all keys in key_status to False.
        Clears all objects in game_objects.
        Resets all player parameters, returns player to the start position.
        Sets game_start time.
        Sets game_state and menu_state to reflect the new game.
        """
        for key in self.key_status:
            self.key_status[key] = False
        del self.game_objects[:]
        self.game_objects = []
        self.player.set_velocity(0, 0)
        self.player.angular_velocity = 0
        self.player.heading = 0
        self.player.reset_position()
        self.game_start = time.time()
        self.game_state = GAME_PLAY
        self.gui.menu_state = MENU_NONE
        self.choose_next_number()

    def update_game(self):
        """
        Progresses all game objects to their new state for the next cycle.

        Spawns new asteroids to replace old and increase challenge progressively.
        Handles Leap Motion input.
        Updates gui and game_objects.
        Checks for object collisions.
        Draws everything to window.
        Updates key inputs.
        """
        # Asteroid Spawn Logic
        game_level = self.game_level()
        if self.count_asteroids() < game_level + 3:  # three asteroids to start, +1 every 15 seconds
            while self.count_asteroids() < 15:  # fifteen asteroids maximum
                self.spawn_asteroid()

        # Leap Motion Logic
        frame = self.controller.frame()  # frame of data from the Leap Motion device
        if len(frame.hands) > 0:  # if a hand is detected
            self.next_bone_index = 0
            self.handle_frame(frame)
            self.test_network()  # check if sign is correct

        self.gui.update(self.current_number,
                        # number of times the current player has successfully signed the requested number
                        dict.database[self.current_user][SUCCESSES_KEY[self.current_number]]
                        if self.current_user is not None else 0)
        self.gui.draw_gui()
        self.move_objects()
        self.check_collisions()
        self.draw_objects()
        self.input_update()

    ####################################################################################################################
    # INPUT HANDLING ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ INPUT HANDLING #
    ####################################################################################################################

    def key_listener(self, event):
        """
        Receives key input from main.

        If game is playing the keys are tracked in key_status.
        If game is not playing (ie menu is open) the keys are passed directly to gui.

        Parameters:
            event (pygame.event): A KEYUP or KEYDOWN event from main.
        """
        if self.game_state == GAME_PLAY:
            if event.type == pygame.KEYDOWN:
                if ord('a') <= event.__dict__["key"] <= ord('z'):
                    self.key_status[event.__dict__["key"]] = True
                elif event.__dict__["key"] == 304:  # Shift
                    self.key_status[event.__dict__["key"]] = True
                elif event.__dict__["key"] == 27:  # Esc
                    exit(0)
            elif event.type == pygame.KEYUP:
                if 97 <= event.__dict__["key"] <= 122:
                    self.key_status[event.__dict__["key"]] = False
                elif event.__dict__["key"] == 304:  # Shift
                    self.key_status[event.__dict__["key"]] = False
                elif event.__dict__["key"] == 32:  # Space bar
                    self.__save_hand()
        elif self.game_state == GAME_MENU:
            self.gui.key_listener(event)

    def mouse_listener(self, event):
        """
        Receives mouse input from main.

        Sends mouse input to gui when the menu is open.

        Parameters:
            event (pygame.event): A MOUSEMOTION, MOUSEBUTTONUP, or MOUSEBUTTONDOWN event from main.
        """
        if self.game_state == GAME_MENU:
            if event.type == pygame.MOUSEMOTION:
                self.gui.mouse_update(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.gui.mouse_click(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                pass

    def input_update(self):
        """
        Applies control functions based on which keys are down.
        """
        if self.key_status[ord('a')]:
            self.player.turn('left')
        if self.key_status[ord('d')]:
            self.player.turn('right')
        if self.key_status[ord('w')]:
            self.player.thrust()
        if self.key_status[304]:  # Shift
            self.player.brake()

    ####################################################################################################################
    # LEAP MOTION HANDLING ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LEAP MOTION HANDLING #
    ####################################################################################################################

    def handle_frame(self, frame):
        """
        Calls handle_finger for each finger of the hand in view of the Leap Motion Device.

        Parameters:
             frame (Leap.frame): All data from the Leap Motion Device.
        """
        hand = frame.hands[0]
        fingers = hand.fingers
        for finger in fingers:
            self.handle_finger(finger)

    def handle_finger(self, finger):
        """
        Calls handle_bone for each bone in finger

        Parameters:
            finger (Leap.finger): Positional data of finger relative to the Leap Motion Device.
        """
        for b in range(4):
            self.handle_bone(finger.bone(b), b)

    def handle_bone(self, bone, bone_type):
        """
        Draws the bone to gui and adds the bone's data to test_data.

        Parameters:
            bone        (Leap.bone):    Positional data of bone relative to the Leap Motion Device.
            bone_type   (int):          Int representing which bone in the finger bone describes.
        """
        base = bone.prev_joint  # joint of current bone that is closest to the wrist
        base = graphics.GUI.leap_to_window(base)  # rescale to be relative to the gui hand_window
        tip = bone.next_joint  # joint of current bone that is furthest from the wrist
        if bone_type == 0 or bone_type == 3:  # only the first knuckle and finger tip are stored in test_data
            self.test_data[0, self.next_bone_index] = bone.next_joint[0]
            self.test_data[0, self.next_bone_index + 1] = bone.next_joint[1]
            self.test_data[0, self.next_bone_index + 2] = bone.next_joint[2]
            self.next_bone_index = self.next_bone_index + 3
        tip = graphics.GUI.leap_to_window(tip)  # rescale to be relative to the gui hand_window
        self.gui.draw_bone(base, tip, bone_type)

    def test_network(self):
        """
        Tests test_data against the training data in classifier.
        """
        if self.game_state == GAME_PLAY:  # only test if game is playing
            self.test_data = utility.center_data(self.test_data)
            # if the current sign matches the current_number
            if self.current_number == self.classifier.Predict(self.test_data):
                self.correct_count -= 1
                if self.correct_count == 0:  # only accept the sign if it is correct for multiple cycles
                    self.success_increment()
                    self.previous_number = self.current_number
                    self.choose_next_number()
                    #
                    # Signing correctly launches a bullet from the player
                    #
                    self.add_bullet()
                    self.correct_count = CORRECT_COUNT  # reset correct_count
            else:
                self.correct_count = CORRECT_COUNT  # reset correct_count

    ####################################################################################################################
    # BASIC GAME FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ BASIC GAME FUNCTIONS #
    ####################################################################################################################

    def switch_users(self, new_user):
        """
        Save dict and load the new user.

        Parameters:
             new_user (str): Name of the new user, key for dict.database
        """
        dict.save()
        self.current_user = dict.login(new_user)

    def choose_next_number(self):
        """
        Randomly chooses the next number, making sure not to pick the previous number.
        """
        while self.current_number == self.previous_number:
            self.current_number = random.randint(0, 9)
        self.attempt_increment()

    def game_level(self):
        """
        Get the current 'game level' as time since game_start divided by fifteen.
        """
        return int(math.floor(self.elapsed_time() / 15))

    def elapsed_time(self):
        """
        Get the time in seconds since game_start
        """
        elapsed = time.time() - self.game_start
        return elapsed

    def attempt_increment(self):
        """
        Increment the number of attempts of current_number by current_user
        """
        if self.current_user is not None:
            dict.database[self.current_user][ATTEMPTS_KEY[self.current_number]] += 1

    def success_increment(self):
        """
        Increment the number of successes of current_number by current_user
        """
        if self.current_user is not None:
            dict.database[self.current_user][SUCCESSES_KEY[self.current_number]] += 1

    def count_asteroids(self):
        """
        Count the number of Asteroids in game_objects.
        """
        count = 0
        for obj in self.game_objects:
            if type(obj) == Asteroid:
                count += 1
        return count

    ####################################################################################################################
    # OBJECT SPAWNING ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ OBJECT SPAWNING #
    ####################################################################################################################

    def add_bullet(self):
        """
        Add a new Bullet at the player's location.
        """
        self.game_objects.append(Bullet(self.player.heading, self.player.position))

    def spawn_asteroid(self):
        """
        Spawn a new Asteroid in a random position off screen.
        """
        self.game_objects.append(Asteroid(GameEngine.__asteroid_position(),
                                                      utility.polar_to_cartesian(GameEngine.__random_velocity()),
                                                      random.randint(- ASTEROID_MAX_ANG_VEL,
                                                                     ASTEROID_MAX_ANG_VEL)))

    def spawn_stars(self):
        """
        Spawn stars in random positions in the game arena.
        """
        for i in range(STAR_COUNT):
            self.background_objects.append(Snow((random.randint(0, GAME_ARENA_DIMENSIONS[0]),
                                                             random.randint(0, GAME_ARENA_DIMENSIONS[1]))))

    ####################################################################################################################
    # OBJECT MOVEMENT AND INTERACTION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ OBJECT MOVEMENT AND INTERACTION #
    ####################################################################################################################

    def move_objects(self):
        """
        Move the player and all objects in game_objects according to their velocity.
        """
        self.player.update()
        for obj in self.game_objects:
            obj.update()
        self.check_collisions()

    def draw_objects(self):
        """
        Draw the player, and all objects in game_objects and background_objects to window.
        """
        self.player.draw_self_to_layer(self.window, 5)
        for obj in self.game_objects:
            obj.draw_self_to_layer(self.window, 4)
        for obj in self.background_objects:
            obj.draw_self_to_layer(self.window, 1)
        self.window.draw()
        self.window.clear()

    def check_collisions(self):
        """
        Check for collisions between Asteroids and Bullets, and between player and Asteroids.
        """
        # for all objects in game_objects
        for object_1 in self.game_objects:
            # if game is playing and object_1 is colliding with player
            if object_1.test_collide(self.player) and self.game_state == GAME_PLAY:
                self.game_state = GAME_MENU
                self.gui.state_change(MENU_OVER)
            # for all OTHER objects in game_objects
            for object_2 in self.game_objects[self.game_objects.index(object_1) + 1:]:
                if object_1.test_collide(object_2):
                    if type(object_1) == Bullet:
                        del object_2
                    else:
                        # TODO fix asteroid collisions
                        pass
                        # game_object.Asteroid.collide_asteroid(asteroid_1, asteroid_2)

    ####################################################################################################################
    # STATIC METHODS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ STATIC METHODS #
    ####################################################################################################################

    @staticmethod
    def __random_velocity():
        """
        Select a random heading and a random magnitude for an Asteriod velocity.

        Returns:
            heading     (int: 0, 360):  Heading in degrees.
            magnitude   (int):          The magnitude of the hypotenuse of the new velocity.
        """
        heading = random.randint(0, 360)
        magnitude = random.randint(ASTEROID_MIN_VEL, ASTEROID_MAX_VEL)
        return heading, magnitude

    @staticmethod
    def __asteroid_position():
        """
        Choose a random position to spawn a new Asteroid.

        Because the game arena width is the game window width + 2 * ASTEROID_MAX_RADIUS,
            spawning the Asteroid between - ASTEROID_MAX_RADIUS and + ASTEROID_MAX_RADIUS will ensure that the Asteroid
            spawns off screen.
        Returns:
            x_pos (int): X value of the new position.
            y_pos (int): Y value of teh new position.
        """
        x_pos = random.randint(- ASTEROID_MAX_RADIUS, ASTEROID_MAX_RADIUS)
        y_pos = random.randint(- ASTEROID_MAX_RADIUS, ASTEROID_MAX_RADIUS)
        return x_pos, y_pos

    ####################################################################################################################
    # DEBUG AND DEVELOPMENT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG AND DEVELOPMENT #
    ####################################################################################################################

    def __save_hand(self):
        """
        Save an example hand image as example_{save_number}.dat, increment save_number.
        """
        if DEBUG:
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
                pickle_out = open("{}{}".format(DATA_PATH, "example_{}.dat".format(self.save_number % 10)),
                                  "wb")
                pickle.dump(gesture_data, pickle_out)
                print "SAVED"
                pickle_out.close()
                self.save_number += 1
