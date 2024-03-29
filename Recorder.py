import sys

sys.path.insert(0, '..')

import Leap
from pygameWindow import PYGAME_WINDOW
import constants
import numpy as np
import pickle
import os


class RECORDER:
    def __init__(self):
        self.controller = Leap.Controller()
        self.pygameWindow = PYGAME_WINDOW()
        self.currentNumberOfHands = 0
        self.previousNumberOfHands = 0
        self.x = 400
        self.y = 400
        self.xMin = 1000
        self.xMax = -1000
        self.yMin = 1000
        self.yMax = -1000
        self.numberOfGestures = 1000
        self.gestureData = np.zeros((5, 4, 6, self.numberOfGestures), dtype='f')
        self.gestureIndex = 0
        to_delete = os.listdir("userData")
        for file in to_delete:
            os.remove("userData/" + file)
        os.rmdir("userData")
        os.mkdir("userData")

    def handle_frame(self, frame):
        hand = frame.hands[0]
        fingers = hand.fingers
        for f in range(5):
            self.handle_finger(fingers[f], f)
        if self.recording():
            print 'gesture ' + str(self.gestureIndex) + ' stored.'
            self.gestureIndex += 1
            if self.gestureIndex == self.numberOfGestures:
                self.save_gesture()
                exit(0)

    def handle_finger(self, finger, f):
        for b in range(4):
            self.handle_bone(finger.bone(b), b, f)

    def handle_bone(self, bone, bone_type, finger_type):
        base = self.handle_vector(bone.prev_joint)
        self.adjust_scale(base)
        base = RECORDER.invert_y(self.scale_point_to_range(base))
        tip = self.handle_vector(bone.next_joint)
        self.adjust_scale(tip)
        tip = RECORDER.invert_y(self.scale_point_to_range(tip))
        self.pygameWindow.draw_line(base, tip, bone_type, self.currentNumberOfHands)
        if self.recording():
            self.gestureData[finger_type, bone_type, 0, self.gestureIndex] = bone.prev_joint[0]
            self.gestureData[finger_type, bone_type, 1, self.gestureIndex] = bone.prev_joint[1]
            self.gestureData[finger_type, bone_type, 2, self.gestureIndex] = bone.prev_joint[2]
            self.gestureData[finger_type, bone_type, 3, self.gestureIndex] = bone.next_joint[0]
            self.gestureData[finger_type, bone_type, 4, self.gestureIndex] = bone.next_joint[1]
            self.gestureData[finger_type, bone_type, 5, self.gestureIndex] = bone.next_joint[2]

    def adjust_scale(self, point):
        if point[0] < self.xMin:
            self.xMin = point[0]
        if point[0] > self.xMax:
            self.xMax = point[0]
        if point[1] < self.yMin:
            self.yMin = point[1]
        if point[1] > self.yMax:
            self.yMax = point[1]

    def save_gesture(self):
        pickle_out = open("userData/gesture.p", "wb")
        pickle.dump(self.gestureData, pickle_out)
        pickle_out.close()

    def scale_point_to_range(self, point):
        new_point = (
            RECORDER.scale_to_range(point[0], self.xMin, self.xMax, 0, constants.PYGAME_WINDOW_WIDTH),
            RECORDER.scale_to_range(point[1], self.yMin, self.yMax, 0, constants.PYGAME_WINDOW_DEPTH)
        )
        return new_point

    def recording(self):
        if self.currentNumberOfHands == 2:
            return True
        return False

    def run_forever(self):
        while True:
            self.pygameWindow.prepare(self.pygameWindow)
            frame = self.controller.frame()
            self.previousNumberOfHands = self.currentNumberOfHands
            self.currentNumberOfHands = len(frame.hands)
            if self.currentNumberOfHands > 0:
                self.handle_frame(frame)
            self.pygameWindow.reveal()

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
    def handle_vector(v):
        tup = (v[0], v[1])
        return tup

    @staticmethod
    def invert_y(point):
        new_point = (point[0], constants.PYGAME_WINDOW_DEPTH - point[1])
        return new_point
