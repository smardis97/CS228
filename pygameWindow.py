import pygame
import constants



class PYGAME_WINDOW:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.pygameWindowWidth, constants.pygameWindowHeight))

    def draw_black_circle(self, x, y):
        pygame.draw.circle(self.screen, (0, 0, 0), (x, y), 15)

    @classmethod
    def prepare(cls, self):
        pygame.event.get()
        self.screen.fill((255, 255, 255))


    @classmethod
    def reveal(cls):
        pygame.display.update()

