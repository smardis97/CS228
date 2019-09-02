import pygame


class PYGAME_WINDOW:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((300, 100))

    @classmethod
    def prepare(cls):
        pygame.event.get()

    @classmethod
    def reveal(cls):
        pass

