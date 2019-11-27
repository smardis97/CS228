import pygame
import constants
import utility
import abc
import settable


class GraphicsEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.PYGAME_WINDOW_WIDTH, constants.PYGAME_WINDOW_DEPTH))
        self.gui = GUI()
        self.layers = [[] for i in range(10)]

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
        self.gui.draw_gui(self.screen)

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
    def __init__(self):
        self.menu_state = constants.MENU_NONE
        self.hand_window = pygame.Rect(constants.HAND_WINDOW_POSITION[settable.HAND_MODE],
                                       (constants.HAND_WINDOW_WIDTH, constants.PYGAME_WINDOW_DEPTH))
        self.buttons = []
        self.labels = []

    def draw_gui(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.hand_window)


class Button:
    def __init__(self, position, size, color, text, highlight, func):
        self.rect = pygame.Rect(position, size)
        self.color = color
        self.highlight = highlight if highlight is not None else color
        self.text = text
        self.action = func

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def contains_mouse(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos[0], mouse_pos[1])

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
