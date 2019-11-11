import pickle
import os
from pygameWindow import PYGAME_WINDOW
import constants
import time


class READER:
    def __init__(self):
        self.numGestures = READER.count_gestures()
        self.pygameWindow = PYGAME_WINDOW()
        self.xMin = 1000
        self.xMax = -1000
        self.yMin = 1000
        self.yMax = -1000

    def print_gestures(self):
        for g in range(self.numGestures):
            pickle_in = open("userData/gesture" + str(g) + ".p", "rb")
            gesture = pickle.load(pickle_in)
            print gesture
            pickle_in.close()

    def draw_gestures(self):
        while True:
            self.draw_each_gesture_once()

    def draw_each_gesture_once(self):
        for g in range(self.numGestures):
            pickle_in = open("userData/gesture" + str(g) + ".p", "rb")
            gesture = pickle.load(pickle_in)
            PYGAME_WINDOW.prepare(self.pygameWindow)
            self.draw_gesture(gesture)
            time.sleep(0.4)
            PYGAME_WINDOW.reveal()
            pickle_in.close()

    def draw_gesture(self, gesture):
        for f in range(5):
            for b in range(4):
                base = (gesture[f, b, 0], gesture[f, b, 1])
                self.adjust_scale(base)
                base = READER.invert_y(self.scale_point_to_range(base))
                tip = (gesture[f, b, 3], gesture[f, b, 4])
                self.adjust_scale(tip)
                tip = READER.invert_y(self.scale_point_to_range(tip))
                self.pygameWindow.draw_black_line(base, tip, b)

    def scale_point_to_range(self, point):
        new_point = (
            READER.scale_to_range(point[0], self.xMin, self.xMax, 0, constants.PYGAME_WINDOW_WIDTH),
            READER.scale_to_range(point[1], self.yMin, self.yMax, 0, constants.PYGAME_WINDOW_DEPTH)
        )
        return new_point

    def adjust_scale(self, point):
        if point[0] < self.xMin:
            self.xMin = point[0]
        if point[0] > self.xMax:
            self.xMax = point[0]
        if point[1] < self.yMin:
            self.yMin = point[1]
        if point[1] > self.yMax:
            self.yMax = point[1]

    @staticmethod
    def scale_to_range(val, init_min, init_max, final_min, final_max):
        init_range = init_max - init_min
        final_range = final_max - final_min
        if init_range == 0:
            new_val = final_min
        else:
            new_val = (((val - init_min) * final_range) / init_range) + final_min
        return int(new_val)

    @staticmethod
    def invert_y(point):
        new_point = (point[0], constants.PYGAME_WINDOW_DEPTH - point[1])
        return new_point

    @staticmethod
    def count_gestures():
        path, dirs, files = next(os.walk('userData'))
        return len(files)
