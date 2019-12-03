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
    def __init__(self, window, parent):
        self.parent = parent
        self.window = window
        self.menu_state = constants.MENU_MAIN
        self.menu_window = pygame.Surface(constants.GUI_WINDOW_DIMENSIONS)
        self.hand_window = pygame.Surface((constants.HAND_WINDOW_WIDTH, constants.PYGAME_WINDOW_DEPTH))
        self.current_number = -1
        self.current_success = 0
        self.opacity = 0
        self.objects = [[], []]
        self.interactable = []
        self.error = ""
        self.labels = []
        self.examples = [pickle.load(open("{}example_{}.dat".format(constants.DATA_PATH, i))) for i in range(10)]
        self.build_gui()

    def clear_error(self):
        self.error = ""

    def set_error(self, message):
        self.error = message
        self.build_gui()

    def state_change(self, new_state):
        self.clear_error()
        self.menu_state = new_state
        self.build_gui()

    def key_listener(self, event):
        if self.menu_state == constants.MENU_LOGIN or self.menu_state == constants.MENU_NEW_CHAR:
            for inter in self.interactable:
                if type(inter) == TextBox:
                    inter.input(event)

    def mouse_update(self, mouse_event):
        for button in self.interactable:
            button.contains_mouse(mouse_event.__dict__['pos'])

    def mouse_click(self, mouse_event):
        for inter in self.interactable:
            inter.click(active=inter.contains_mouse(mouse_event.__dict__['pos']),
                        engine=self.parent, gui=self, mstate=self.menu_state)

    def build_gui(self):
        del self.interactable[:]
        self.interactable = []
        del self.labels[:]
        self.labels = []
        if self.menu_state == constants.MENU_MAIN:
            button_x_pos = constants.GUI_WINDOW_DIMENSIONS[0] / 2
            button_y_start = constants.GUI_WINDOW_DIMENSIONS[1] / 2
            button_y_interval = constants.BUTTON_DIMENSIONS[1] + 10

            self.labels.append(Label((constants.GUI_WINDOW_DIMENSIONS[0] / 2, 30),
                                     constants.GUI_LABEL_TEXT_COLOR, "MAIN MENU"))

            self.interactable.append(Button((button_x_pos, button_y_start),
                                            "NEW GAME",
                                            buttons.play))

            self.interactable.append(Button((button_x_pos, button_y_start + button_y_interval),
                                            "LOGIN",
                                            buttons.login))

            self.interactable.append(Button((button_x_pos, button_y_start + 2 * button_y_interval),
                                            "NEW PROFILE",
                                            buttons.new_char))

            self.interactable.append(Button((button_x_pos, button_y_start + 3 * button_y_interval),
                                            "SETTINGS",
                                            buttons.settings))

            self.interactable.append(Button((button_x_pos, button_y_start + 4 * button_y_interval),
                                            "EXIT",
                                            buttons.quit_button))
        elif self.menu_state == constants.MENU_LOGIN:
            menu_center_x = constants.GUI_WINDOW_DIMENSIONS[0] / 2
            menu_center_y = constants.GUI_WINDOW_DIMENSIONS[1] / 2
            button_y_interval = constants.BUTTON_DIMENSIONS[1] + 10

            self.labels.append(Label((menu_center_x, 30),
                                     constants.GUI_LABEL_TEXT_COLOR, "PROFILE LOGIN"))

            self.labels.append(Label((menu_center_x, menu_center_y - button_y_interval),
                                     constants.GUI_ERROR_TEXT_COLOR, self.error))

            self.interactable.append(Button((menu_center_x, menu_center_y),
                                            "NEW PROFILE",
                                            buttons.new_char))

            self.interactable.append(Button((menu_center_x, menu_center_y + button_y_interval),
                                            "CONFIRM",
                                            buttons.text_confirm))

            self.interactable.append(Button((menu_center_x, menu_center_y + 2 * button_y_interval),
                                            "CANCEL",
                                            buttons.cancel))

            self.interactable.append(TextBox((menu_center_x, menu_center_y - menu_center_y / 2)))
        elif self.menu_state == constants.MENU_NEW_CHAR:
            menu_center_x = constants.GUI_WINDOW_DIMENSIONS[0] / 2
            menu_center_y = constants.GUI_WINDOW_DIMENSIONS[1] / 2
            button_y_interval = constants.BUTTON_DIMENSIONS[1] + 10

            self.labels.append(Label((menu_center_x, 30),
                                     constants.GUI_LABEL_TEXT_COLOR, "NEW PROFILE"))

            self.labels.append(Label((menu_center_x, menu_center_y - button_y_interval),
                                     constants.GUI_ERROR_TEXT_COLOR, self.error))

            self.interactable.append(Button((menu_center_x, menu_center_y + button_y_interval),
                                            "CONFIRM",
                                            buttons.text_confirm))

            self.interactable.append(Button((menu_center_x, menu_center_y + 2 * button_y_interval),
                                            "CANCEL",
                                            buttons.cancel))

            self.interactable.append(TextBox((menu_center_x, menu_center_y - menu_center_y / 2)))
        elif self.menu_state == constants.MENU_SETTINGS:
            pass
        elif self.menu_state == constants.MENU_OVER:
            menu_center_x = constants.GUI_WINDOW_DIMENSIONS[0] / 2
            menu_center_y = constants.GUI_WINDOW_DIMENSIONS[1] / 2
            button_y_interval = constants.BUTTON_DIMENSIONS[1] + 10

            self.labels.append(Label((menu_center_x, 30),
                                     constants.GUI_ERROR_TEXT_COLOR, "GAME OVER"))

            self.interactable.append(Button((menu_center_x, menu_center_y),
                                            "NEW GAME",
                                            buttons.play))

            self.interactable.append(Button((menu_center_x, menu_center_y + button_y_interval),
                                            "MAIN MENU",
                                            buttons.cancel))

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
        for layer in self.objects:
            for obj in layer:
                obj.draw(self.hand_window)
        self.window.screen.blit(self.hand_window, constants.HAND_WINDOW_POSITION[settable.HAND_MODE])
        if self.menu_state is not constants.MENU_NONE:
            for label in self.labels:
                self.menu_window.blit(label.draw(), label.get_position())
            for inter in self.interactable:
                self.menu_window.blit(inter.draw(), inter.get_position())
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


class MenuObject:
    __metaclass__ = abc.ABCMeta

    def __init__(self, position, color):
        self.position = position
        self.color = color

    @abc.abstractmethod
    def get_position(self):
        return NotImplemented

    @abc.abstractmethod
    def draw(self):
        return NotImplemented

    @abc.abstractmethod
    def contains_mouse(self, mouse_pos):
        return NotImplemented

    @abc.abstractmethod
    def click(self, active=False, **kwargs):
        return NotImplemented


class Button(MenuObject):
    def __init__(self, position, text, func, color=constants.GUI_BUTTON_COLOR, highlight=constants.GUI_BUTTON_HIGHLIGHT):
        MenuObject.__init__(self, position, color)
        self.absolute_pos = utility.vector_add(constants.GUI_WINDOW_POSITION, self.get_position())
        self.rect = pygame.Surface(constants.BUTTON_DIMENSIONS)
        self.text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(),
                                                             constants.BUTTON_LABEL_SIZE
                                                             ),
                                            text, True, constants.GUI_BUTTON_TEXT_COLOR)
        self.highlight = highlight if highlight is not None else color
        self.action = func
        self.hover = False

    def draw(self):
        color = self.color if not self.hover else self.highlight
        self.rect.fill(color)
        self.rect.blit(self.text, self.text_offset())
        return self.rect

    def get_position(self):
        return self.position[0] - (constants.BUTTON_DIMENSIONS[0] / 2), \
               self.position[1] - (constants.BUTTON_DIMENSIONS[1] / 2)

    def text_offset(self):
        x_offset = (self.rect.get_size()[0] / 2) - (self.text.get_size()[0] / 2)
        y_offset = (self.rect.get_size()[1] / 2) - (self.text.get_size()[1] / 2)
        return x_offset, y_offset

    def contains_mouse(self, mouse_pos):
        top_left_corner = self.absolute_pos
        bottom_right_corner = utility.vector_add(self.absolute_pos, self.rect.get_size())
        x_contains = top_left_corner[0] <= mouse_pos[0] <= bottom_right_corner[0]
        y_contains = top_left_corner[1] <= mouse_pos[1] <= bottom_right_corner[1]
        self.hover = x_contains and y_contains
        return self.hover

    def click(self, active=False, **kwargs):
        if active:
            return self.action(**kwargs)


class Label(MenuObject):
    def __init__(self, position, color, text):
        MenuObject.__init__(self, position, color)
        self.text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), constants.MENU_LABEL_SIZE),
                                            text, True, self.color)

    def draw(self):
        return self.text

    def get_position(self):
        return self.position[0] - (self.text.get_size()[0] / 2), self.position[1] - (self.text.get_size()[1] / 2)

    def contains_mouse(self, mouse_pos):
        return False

    def click(self, active=False, **kwargs):
        pass


class TextBox(MenuObject):
    def __init__(self, position, color=constants.TEXT_BOX_COLOR, highlight=constants.TEXT_BOX_HIGHLIGHT, activec=constants.TEXT_BOX_ACTIVE):
        MenuObject.__init__(self, position, color)
        self.absolute_pos = utility.vector_add(constants.GUI_WINDOW_POSITION, self.get_position())
        self.rect = pygame.Surface(constants.TEXT_BOX_DIMENSIONS)
        self.text_content = ""
        self.highlight = highlight
        self.active_color = activec
        self.hover = False
        self.active = False

    def input(self, key_event):
        if key_event.type == pygame.KEYDOWN:
            if key_event.__dict__['key'] == 8:
                if len(self.text_content) > 0:
                    self.text_content = self.text_content[:-1]
            elif 'unicode' in key_event.__dict__:
                self.text_content += key_event.__dict__['unicode']

    def draw(self):
        self.rect.fill(self.get_color())
        self.rect.blit(self.get_text(), self.text_offset())
        return self.rect

    def get_position(self):
        return self.position[0] - (constants.TEXT_BOX_DIMENSIONS[0] / 2), \
               self.position[1] - (constants.TEXT_BOX_DIMENSIONS[1] / 2)

    def get_color(self):
        if self.active:
            color = self.active_color
        elif self.hover:
            color = self.highlight
        else:
            color = self.color
        return color

    def get_text(self):
        return pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), constants.TEXT_BOX_TEXT_SIZE),
                                       self.text_content, True, constants.TEXT_BOX_TEXT_COLOR)

    def text_offset(self):
        x_offset = (self.rect.get_size()[0] / 2) - (self.get_text().get_size()[0] / 2)
        y_offset = (self.rect.get_size()[1] / 2) - (self.get_text().get_size()[1] / 2)
        return x_offset, y_offset

    def contains_mouse(self, mouse_pos):
        top_left_corner = self.absolute_pos
        bottom_right_corner = utility.vector_add(self.absolute_pos, self.rect.get_size())
        x_contains = top_left_corner[0] <= mouse_pos[0] <= bottom_right_corner[0]
        y_contains = top_left_corner[1] <= mouse_pos[1] <= bottom_right_corner[1]
        self.hover = x_contains and y_contains
        return self.hover

    def click(self, active=False, **kwargs):
        self.active = active


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
