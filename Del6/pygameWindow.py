import pygame
import constants


class PYGAME_WINDOW:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.pygameWindowWidth, constants.pygameWindowHeight))
        self.disp_counter = 10

    def draw_black_circle(self, x, y):
        pygame.draw.circle(self.screen, (0, 0, 0), (x, y), 15)

    def draw_black_line(self, base, tip, bone_type):
        pygame.draw.line(self.screen, (0, 0, 0), base, tip, 2 * (3 - bone_type) + 1)

    def draw_line(self, base, tip, bone_type, hand_status):
        if hand_status == 1:
            pygame.draw.line(self.screen, (0, 255, 0), base, tip, 2 * (3 - bone_type) + 1)
        else:
            pygame.draw.line(self.screen, (255, 0, 0), base, tip, 2 * (3 - bone_type) + 1)

    def draw_dividers(self):
        pygame.draw.line(self.screen, (0, 0, 0),
                         (constants.pygameWindowWidth / 2, 0),
                         (constants.pygameWindowWidth / 2, constants.pygameWindowHeight), 7)
        pygame.draw.line(self.screen, (0, 0, 0),
                         (0, constants.pygameWindowHeight / 2),
                         (constants.pygameWindowWidth, constants.pygameWindowHeight / 2), 7)

    def draw_help_image(self, hand_present=False, (lr, ud)=(None, None)):
        if hand_present:
            if lr > 0:
                image = pygame.image.load("Del6/images/direct-left.jpg")
                self.disp_counter = 10
            elif lr < 0:
                image = pygame.image.load("Del6/images/direct-right.jpg")
                self.disp_counter = 10
            else:
                if ud > 0:
                    image = pygame.image.load("Del6/images/direct-down.jpg")
                    self.disp_counter = 10
                elif ud < 0:
                    image = pygame.image.load("Del6/images/direct-up.jpg")
                    self.disp_counter = 10
                elif self.disp_counter > 0:
                    image = pygame.image.load("Del6/images/success.jpg")
                    self.disp_counter -= 1
                else:
                    return True

        else:
            image = pygame.image.load("Del6/images/place-in-view.jpg")
            self.disp_counter = 10
        self.screen.blit(image, (constants.pygameWindowWidth / 2 + 3, -3))
        return False

    def draw_example(self, number):
        if number > 9 or number < 0:
            raise IndexError
        else:
            file_name = "Del6/images/asl-" + str(number) + ".png"
            image = pygame.image.load(file_name)
            self.screen.blit(image,
                             (constants.pygameWindowWidth * 0.75 - (image.get_width() / 2),
                              constants.pygameWindowHeight / 2))

    @classmethod
    def prepare(cls, self):
        pygame.event.get()
        self.screen.fill((255, 255, 255))


    @classmethod
    def reveal(cls):
        pygame.display.update()
