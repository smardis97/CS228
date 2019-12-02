import pygame
import pickle
import constants
import utility
import abc
import settable
import buttons


class GraphicsEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.PYGAME_WINDOW_WIDTH, constants.PYGAME_WINDOW_DEPTH))
        self.layers = [[] for i in range(10)]

    def draw_example_bone(self, base, tip, bone_type):
        pass

    def add_to_layer(self, layer, obj):
        if 0 <= layer < 10:
            self.layers[layer].append(obj)
        else:
            raise IndexError

    def clear(self):
        for layer in self.layers:
            for obj in layer:
                del obj
            del layer[:]
        self.layers = [[] for i in range(10)]

    def draw(self):
        for layer in self.layers:
            for obj in layer:
                obj.draw(self.screen)

    @staticmethod
    def arena_to_window(point):
        new_point = (point[0] - constants.ASTEROID_MAX_RADIUS + constants.GAME_WINDOW_LEFT_EDGE[settable.HAND_MODE],
                     point[1] - constants.ASTEROID_MAX_RADIUS)
        return new_point

    @classmethod
    def prepare(cls, self):
        pygame.event.get()
        self.screen.fill((0, 0, 0))

    @classmethod
    def reveal(cls):
        pygame.display.update()


class GUI:
    def __init__(self, window):
        self.window = window
        self.menu_state = constants.MENU_MAIN
        self.menu_window = pygame.Surface(constants.GUI_WINDOW_DIMENSIONS)
        self.menu_window.fill((0, 0, 0))
        self.hand_window = pygame.Surface((constants.HAND_WINDOW_WIDTH, constants.PYGAME_WINDOW_DEPTH), pygame.SRCALPHA)
        self.hand_window.fill((255, 255, 255))
        self.current_number = -1
        self.current_success = 0
        self.opacity = 0
        self.objects = [[], []]
        self.buttons = []
        self.labels = []
        self.examples = [pickle.load(open("{}example_{}.dat".format(constants.DATA_PATH, i))) for i in range(10)]
        self.build_gui()

    def state_change(self, new_state):
        self.menu_state = new_state
        self.build_gui()

    def mouse_update(self, mouse_event):
        for button in self.buttons:
            button.contains_mouse(mouse_event.__dict__['pos'])

    def mouse_click(self, mouse_event):
        for button in self.buttons:
            if button.contains_mouse(mouse_event.__dict__['pos']):
                button.click()

    def build_gui(self):
        del self.buttons[:]
        self.buttons = []
        del self.labels[:]
        self.labels = []
        if self.menu_state == constants.MENU_MAIN:
            self.buttons.append(Button((50, 50), constants.GUI_BUTTON_COLOR, "TEST", buttons.play, constants.GUI_BUTTON_HIGHLIGHT))
        elif self.menu_state == constants.MENU_LOGIN:
            pass
        elif self.menu_state == constants.MENU_NEW_CHAR:
            pass
        elif self.menu_state == constants.MENU_SETTINGS:
            pass
        else:
            pass

    def add_object(self, obj, i):
        self.objects[i].append(obj)

    def draw_example(self):
        example = self.examples[self.current_number]
        for f in range(5):
            for b in range(4):
                base = GUI.leap_to_window(example[f][b][0])
                tip = GUI.leap_to_window(example[f][b][1])
                self.draw_example_bone(base, tip, b)

    def clear(self):
        del self.objects[:]
        self.objects = [[], []]

    def update(self, current, success):
        self.opacity = min([100 + 10 * self.current_success, 255])
        self.current_number = current
        self.current_success = success
        self.draw_example()

    def draw_gui(self):
        self.menu_window.fill(constants.GUI_WINDOW_COLOR)
        self.hand_window.fill(constants.HAND_WINDOW_COLOR)
        text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), 40),
                                       str(self.current_number), True, (0, 0, 0))
        self.hand_window.blit(text, (10, 10))
        for list in self.objects:
            for obj in list:
                obj.draw(self.hand_window)
        self.window.screen.blit(self.hand_window, constants.HAND_WINDOW_POSITION[settable.HAND_MODE])
        for button in self.buttons:
            self.menu_window.blit(button.draw(), button.position)
        self.window.screen.blit(self.menu_window, constants.GUI_WINDOW_POSITION)
        self.clear()

    def draw_example_bone(self, base, tip, bone_type):
        self.add_object(Line(base, tip, (self.opacity, self.opacity, self.opacity), 4 * (3 - bone_type) + 2), 0)

    def draw_bone(self, base, tip, bone_type):
        self.add_object(Line(base, tip, (0, 0, 0), 2 * (3 - bone_type) + 1), 1)

    @staticmethod
    def leap_to_window(point):
        new_point = (
            utility.scale_to_range(point[0], constants.LEAP_VISION_MIN_COORDS[0], constants.LEAP_VISION_MAX_COORDS[0],
                                   - constants.HAND_GRAPHICAL_CENTER[0],
                                   constants.HAND_REGION_DIMENSIONS[0] - constants.HAND_GRAPHICAL_CENTER[0])
            + constants.HAND_CENTERING_ADJUST[0],
            utility.scale_to_range(point[2], constants.LEAP_VISION_MIN_COORDS[2], constants.LEAP_VISION_MAX_COORDS[2],
                                   - constants.HAND_GRAPHICAL_CENTER[1],
                                   constants.HAND_REGION_DIMENSIONS[1] - constants.HAND_GRAPHICAL_CENTER[1])
            + constants.HAND_CENTERING_ADJUST[1]
        )
        return new_point


class Button:
    def __init__(self, position, color, text, func, highlight=None):
        self.position = position
        self.absolute_pos = utility.vector_add(constants.GUI_WINDOW_POSITION, self.position)
        self.rect = pygame.Surface(constants.BUTTON_DIMENSIONS)
        self.text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(),
                                                             constants.BUTTON_LABEL_SIZE
                                                             ),
                                            text, True, constants.GUI_BUTTON_TEXT_COLOR)
        self.color = color
        self.highlight = highlight if highlight is not None else color
        self.action = func
        self.hover = False

    def draw(self):
        color = self.color if not self.hover else self.highlight
        self.rect.fill(color)
        self.rect.blit(self.text, constants.BUTTON_LABEL_OFFSET)
        return self.rect

    def contains_mouse(self, mouse_pos):
        top_left_corner = self.absolute_pos
        bottom_right_corner = utility.vector_add(self.absolute_pos, self.rect.get_size())
        x_contains = top_left_corner[0] <= mouse_pos[0] <= bottom_right_corner[0]
        y_contains = top_left_corner[1] <= mouse_pos[1] <= bottom_right_corner[1]
        self.hover = x_contains and y_contains
        return self.hover

    def click(self, **kwargs):
        return self.action(**kwargs)


class GraphicsObject:
    __metaclass__ = abc.ABCMeta

    def __init__(self, color, thickness):
        self.color = color
        self.thickness = thickness

    @abc.abstractmethod
    def draw(self, screen):
        return NotImplemented


class Line(GraphicsObject):
    def __init__(self, start, end, color=(255, 255, 255), thickness=1):
        GraphicsObject.__init__(self, color, thickness)
        self.start = start
        self.end = end

    def draw(self, screen):
        pygame.draw.line(screen, self.color, GraphicsEngine.arena_to_window(self.start),
                         GraphicsEngine.arena_to_window(self.end), self.thickness)


class Circle(GraphicsObject):
    def __init__(self, center, radius, color=(255, 255, 255), thickness=0):
        GraphicsObject.__init__(self, color, thickness)
        self.center = utility.tuple_float_to_int(center)
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, GraphicsEngine.arena_to_window(self.center),
                           self.radius, self.thickness)


class Rectangle(GraphicsObject):
    def __init__(self, position, dimensions, color):
        GraphicsObject.__init__(self, color, 0)
        self.rect = pygame.Rect(position, dimensions)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
