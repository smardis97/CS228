import settable
import pygame

PYGAME_WINDOW_WIDTH = 1280
PYGAME_WINDOW_DEPTH = 768

RIGHT_MODE = "RIGHT"
LEFT_MODE = "LEFT"

WINDOW_BOTTOM = PYGAME_WINDOW_DEPTH
WINDOW_TOP = 0

GAME_WINDOW_RIGHT_EDGE = {
    RIGHT_MODE: 2 * PYGAME_WINDOW_WIDTH / 3,
    LEFT_MODE: PYGAME_WINDOW_WIDTH
}
GAME_WINDOW_LEFT_EDGE = {
    RIGHT_MODE: 0,
    LEFT_MODE: PYGAME_WINDOW_WIDTH / 3
}
DISPLAY_WINDOW_RIGHT_EDGE = {
    RIGHT_MODE: PYGAME_WINDOW_WIDTH,
    LEFT_MODE: PYGAME_WINDOW_WIDTH / 3
}
DISPLAY_WINDOW_LEFT_EDGE = {
    RIGHT_MODE: 2 * PYGAME_WINDOW_WIDTH / 3,
    LEFT_MODE: 0
}
GUI_WINDOW_RIGHT_EDGE = NotImplemented
GUI_WINDOW_LEFT_EDGE = NotImplemented
GUI_WINDOW_TOP_EDGE = NotImplemented
GUI_WINDOW_BOTTOM_EDGE = NotImplemented

# Game Logic

CIRCLE_DEG = 360.

GAME_MENU = "MENU"
GAME_PLAY = "PLAY"
GAME_OVER = "OVER"

MENU_MAIN = "MAIN"
MENU_NEW_CHAR = "NEW"
MENU_LOGIN = "LOGIN"
MENU_SETTINGS = "SETTINGS"

PLAYER_MAX_VEL = 25
ASTEROID_MAX_VEL = 20
STAR_MAX_VEL = 10

PLAYER_MAX_ANG_VEL = 20
ASTEROID_MAX_ANG_VEL = 5
STAR_MAX_ANG_VEL = 0

PLAYER_GRAPHIC_POSITION = {
    RIGHT_MODE: (GAME_WINDOW_RIGHT_EDGE[RIGHT_MODE] / 2, WINDOW_BOTTOM / 2),
    LEFT_MODE: (GAME_WINDOW_RIGHT_EDGE[LEFT_MODE] - GAME_WINDOW_LEFT_EDGE[LEFT_MODE], WINDOW_BOTTOM / 2)
}
PLAYER_THICKNESS = 3
PLAYER_MAX_RADIUS = 20
PLAYER_COLLIDE_RADIUS = 15
PLAYER_ACCELERATION = 2
PLAYER_ANGULAR_ACCELERATION = 3

PLAYER_COLORS = [
    pygame.color.THECOLORS['red1'],
    pygame.color.THECOLORS['blue1'],
    pygame.color.THECOLORS['green1'],
    pygame.color.THECOLORS['yellow1']
]

ASTEROID_MAX_VERTICES = 15
ASTEROID_MIN_VERTICES = 7
ASTEROID_MAX_RADIUS = 40
ASTEROID_MIN_RADIUS = 25
ASTEROID_THICKNESS = 1
STAR_MIN_RADIUS = 1
STAR_MAX_RADIUS = 3

# File Path Parts
PARENT_DIR = "GameFinal/"
IMAGES_DIR = "images/"
DATA_DIR = "userData/"

PATH_TO_PROJECT = "/Users/Stover/Documents/LeapSDK/lib/CS228/"
IMAGES_PATH = "{}{}".format(PARENT_DIR, IMAGES_DIR)
DATA_PATH = "{}{}".format(PARENT_DIR, DATA_DIR)

NN_CLASSIFIER_FILE = "classifier.p"
USER_DATABASE_FILE = "database.p"

TRAIN_0_FILE = "Clark_train0.p"
TEST_0_FILE = "Clark_test0.p"
TRAIN_0_FILE_LEFT = "Clark_train0_left.p"
TEST_0_FILE_LEFT = "Clark_test0_left.p"

TRAIN_1_FILE = "Newton_train1.p"
TEST_1_FILE = "Newton_test1.p"
TRAIN_1_FILE_LEFT = "Giroux_train1_left.p"
TEST_1_FILE_LEFT = "Giroux_test1_left.p"

TRAIN_2_FILE = "Apple_train2.p"
TEST_2_FILE = "Apple_test2.p"
TRAIN_2_FILE_LEFT = "Giroux_train2_left.p"
TEST_2_FILE_LEFT = "Giroux_test2_left.p"

TRAIN_3_FILE = "Apple_train3.p"
TEST_3_FILE = "Apple_test3.p"
TRAIN_3_FILE_LEFT = "Gordon_train3_left.p"
TEST_3_FILE_LEFT = "Gordon_test3_left.p"

TRAIN_4_FILE = "Deluca_train4.p"
TEST_4_FILE = "Deluca_test4.p"
TRAIN_4_FILE_LEFT = "Ogilvie_train4_left.p"
TEST_4_FILE_LEFT = "Ogilvie_test4_left.p"

TRAIN_5_FILE = "Deluca_train5.p"
TEST_5_FILE = "Deluca_test5.p"
TRAIN_5_FILE_LEFT = "Warren_train5_left.p"
TEST_5_FILE_LEFT = "Warren_test5_left.p"

TRAIN_6_FILE = "Boland_train6.p"
TEST_6_FILE = "Boland_test6.p"
TRAIN_6_FILE_LEFT = "Wu_train6_left.p"
TEST_6_FILE_LEFT = "Wu_test6_left.p"

TRAIN_7_FILE = "Erickson_train7.p"
TEST_7_FILE = "Erickson_test7.p"
TRAIN_7_FILE_LEFT = "Erickson_train7_left.p"
TEST_7_FILE_LEFT = "Erickson_test7_left.p"

TRAIN_8_FILE = "Erickson_train8.p"
TEST_8_FILE = "Erickson_test8.p"
TRAIN_8_FILE_LEFT = "Burleson_train8_left.p"
TEST_8_FILE_LEFT = "Burleson_test8_left.p"

TRAIN_9_FILE = "Lee_train9.p"
TEST_9_FILE = "Lee_test9.p"
TRAIN_9_FILE_LEFT = "Childs_train9_left.p"
TEST_9_FILE_LEFT = "Childs_test9_left.p"
