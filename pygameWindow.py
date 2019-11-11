import pygame
import constants



class PYGAME_WINDOW:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.PYGAME_WINDOW_WIDTH, constants.PYGAME_WINDOW_DEPTH))

    def draw_black_circle(self, x, y):
        pygame.draw.circle(self.screen, (0, 0, 0), (x, y), 15)

    def draw_black_line(self, base, tip, bone_type):
        pygame.draw.line(self.screen, (0, 0, 0), base, tip, 2 * (3 - bone_type) + 1)

    def draw_line(self, base, tip, bone_type, hand_status):
        if hand_status == 1:
            pygame.draw.line(self.screen, (0, 255, 0), base, tip, 2 * (3 - bone_type) + 1)
        else:
            pygame.draw.line(self.screen, (255, 0, 0), base, tip, 2 * (3 - bone_type) + 1)

    @classmethod
    def prepare(cls, self):
        pygame.event.get()
        self.screen.fill((255, 255, 255))


    @classmethod
    def reveal(cls):
        pygame.display.update()
