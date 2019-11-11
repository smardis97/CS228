import pygame
import constants
import utility
import numpy as np


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

    def draw_secondary_dividers(self):
        pygame.draw.line(self.screen, (0, 0, 0),
                         (3 * constants.pygameWindowWidth / 8, constants.pygameWindowHeight / 2),
                         (3 * constants.pygameWindowWidth / 8, constants.pygameWindowHeight), 4)
        pygame.draw.line(self.screen, (0, 0, 0),
                         (0, 3 * constants.pygameWindowHeight / 4),
                         (3 * constants.pygameWindowWidth / 8, 3 * constants.pygameWindowHeight / 4), 4)

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

    def draw_example(self, number, level=0):
        draw_image = True
        if number > 9 or number < 0:
            raise IndexError
        else:
            if level >= 15:
                draw_image = False
            elif level >= 12:
                if number <= 7:
                    draw_image = False
            elif level >= 8:
                if number <= 4:
                    draw_image = False
            elif level >= 5:
                if number <= 2:
                    draw_image = False
            if draw_image:
                file_name = "Del6/images/asl-" + str(number) + ".png"
                image = pygame.image.load(file_name)
                self.screen.blit(image,
                                 (constants.pygameWindowWidth * 0.75 - (image.get_width() / 2),
                                  constants.pygameWindowHeight / 2))
            else:
                text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), 80),
                                               str(number), True, [0, 0, 0])
                self.screen.blit(text, (constants.pygameWindowWidth * 0.75, constants.pygameWindowHeight * 0.75))

    def draw_attempts(self, attempts_tenple):
        for i in range(10):
            text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), 30),
                                           str(i) + " attempts: " + str(attempts_tenple[i]), True, [0, 0, 0])
            self.screen.blit(text, (7, 5 + (constants.pygameWindowHeight / 2) + 30 * i))

    def draw_successes(self, attempts_tenple):
        for i in range(10):
            text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), 30),
                                           str(i) + " successes: " + str(attempts_tenple[i]), True, [0, 0, 0])
            self.screen.blit(text, (7, 5 + (constants.pygameWindowHeight / 2) + 30 * i))

    def draw_user_visualization(self, user, current_target):
        target_times = self.get_target_times(user, current_target)
        if len(target_times) > 0:
            for i in range(len(target_times)):
                pygame.draw.circle(self.screen, (0, 0, 0),
                                   self.graphable_point(target_times[i], i, max(target_times), len(target_times)), 3)
                if i != len(target_times) - 1:
                    pygame.draw.line(self.screen, (0, 0, 0),
                                     self.graphable_point(target_times[i], i, max(target_times), len(target_times)),
                                     self.graphable_point(target_times[i+1], i+1, max(target_times), len(target_times)), 2)

        else:
            pass

    def graphable_point(self, value, number, max_val, length):
        x = utility.scale_to_range(number, 0, length,
                                   utility.scale_to_range(10, 0, 100, 0, 3 * constants.pygameWindowWidth / 8),
                                   utility.scale_to_range(90, 0, 100, 0, 3 * constants.pygameWindowWidth / 8)) + 3

        y = utility.scale_to_range(value, 0, max_val,
                                   utility.scale_to_range(90, 0, 100, constants.pygameWindowHeight / 2, 3 * constants.pygameWindowHeight / 4),
                                   utility.scale_to_range(10, 0, 100, constants.pygameWindowHeight / 2, 3 * constants.pygameWindowHeight / 4))

        return x, y

    def draw_axes(self):
        # Y-axis
        pygame.draw.line(self.screen, (0, 0, 0),
                         (utility.scale_to_range(10, 0, 100, 0, 3 * constants.pygameWindowWidth / 8),
                          utility.scale_to_range(10, 0, 100, constants.pygameWindowHeight / 2, 3 * constants.pygameWindowHeight / 4)),
                         (utility.scale_to_range(10, 0, 100, 0, 3 * constants.pygameWindowWidth / 8),
                          utility.scale_to_range(90, 0, 100, constants.pygameWindowHeight / 2, 3 * constants.pygameWindowHeight / 4)),
                         2)
        # X-axis
        pygame.draw.line(self.screen, (0, 0, 0),
                         (utility.scale_to_range(10, 0, 100, 0, 3 * constants.pygameWindowWidth / 8),
                          utility.scale_to_range(90, 0, 100, constants.pygameWindowHeight / 2, 3 * constants.pygameWindowHeight / 4)),
                         (utility.scale_to_range(90, 0, 100, 0, 3 * constants.pygameWindowWidth / 8),
                          utility.scale_to_range(90, 0, 100, constants.pygameWindowHeight / 2, 3 * constants.pygameWindowHeight / 4)),
                         2)

        # Y-axis
        pygame.draw.line(self.screen, (0, 0, 0),
                         (utility.scale_to_range(10, 0, 100, 0, 3 * constants.pygameWindowWidth / 8),
                          utility.scale_to_range(10, 0, 100, 3 * constants.pygameWindowHeight / 4, constants.pygameWindowHeight)),
                         (utility.scale_to_range(10, 0, 100, 0, 3 * constants.pygameWindowWidth / 8),
                          utility.scale_to_range(90, 0, 100, 3 * constants.pygameWindowHeight / 4, constants.pygameWindowHeight)),
                         2)
        # X-axis
        pygame.draw.line(self.screen, (0, 0, 0),
                         (utility.scale_to_range(10, 0, 100, 0, 3 * constants.pygameWindowWidth / 8),
                          utility.scale_to_range(90, 0, 100, 3 * constants.pygameWindowHeight / 4, constants.pygameWindowHeight)),
                         (utility.scale_to_range(90, 0, 100, 0, 3 * constants.pygameWindowWidth / 8),
                          utility.scale_to_range(90, 0, 100, 3 * constants.pygameWindowHeight / 4, constants.pygameWindowHeight)),
                         2)

    def get_target_times(self, user, target):
        return user["times" + str(target)]

    def get_all_times(self, user):
        all_times = []
        for i in range(10):
            all_times.extend(user["times" + str(i)])
        return all_times

    # Some massive fucking spaghetti code is what this is
    def draw_group_visualization(self, users, current_user_name):
        all_other_times = []
        for name, data in users.iteritems():
            if name != current_user_name:
                all_other_times.extend(self.get_all_times(data))
        others_mean = np.mean(all_other_times)
        user_mean = np.mean(self.get_all_times(users[current_user_name]))
        pygame.draw.line(self.screen, pygame.color.THECOLORS['blue'],
                         (utility.scale_to_range(10, 0, 100, 0, 3 * constants.pygameWindowWidth / 8),
                          utility.scale_to_range(1, 0, 4,
                                                 utility.scale_to_range(10, 0, 100, 3 * constants.pygameWindowHeight / 4, constants.pygameWindowHeight),
                                                 utility.scale_to_range(90, 0, 100, 3 * constants.pygameWindowHeight / 4, constants.pygameWindowHeight)
                                                 )
                          ),

                         (utility.scale_to_range(user_mean, 0, 1.5 * max([others_mean, user_mean]), 0 , 3 * constants.pygameWindowWidth / 8),
                          utility.scale_to_range(1, 0, 4,
                                                 utility.scale_to_range(10, 0, 100, 3 * constants.pygameWindowHeight / 4, constants.pygameWindowHeight),
                                                 utility.scale_to_range(90, 0, 100, 3 * constants.pygameWindowHeight / 4, constants.pygameWindowHeight)
                                                 )
                          ), 20)

        pygame.draw.line(self.screen, pygame.color.THECOLORS['gray'],
                         (utility.scale_to_range(10, 0, 100, 0, 3 * constants.pygameWindowWidth / 8),
                          utility.scale_to_range(3, 0, 4,
                                                 utility.scale_to_range(10, 0, 100, 3 * constants.pygameWindowHeight / 4, constants.pygameWindowHeight),
                                                 utility.scale_to_range(90, 0, 100, 3 * constants.pygameWindowHeight / 4, constants.pygameWindowHeight)
                                                 )
                          ),

                         (utility.scale_to_range(others_mean, 0, 1.5 * max([others_mean, user_mean]), 0, 3 * constants.pygameWindowWidth / 8),
                          utility.scale_to_range(3, 0, 4,
                                                 utility.scale_to_range(10, 0, 100, 3 * constants.pygameWindowHeight / 4, constants.pygameWindowHeight),
                                                 utility.scale_to_range(90, 0, 100, 3 * constants.pygameWindowHeight / 4, constants.pygameWindowHeight)
                                                 )
                          ), 20)

    def draw_help_visualization(self, warmer):
        if warmer:
            image = pygame.image.load("Del6/images/checkmark.jpg")
            self.screen.blit(image, (3 * constants.pygameWindowWidth / 8, constants.pygameWindowHeight / 2))
        else:
            image = pygame.image.load("Del6/images/x.jpg")
            self.screen.blit(image, (3 * constants.pygameWindowWidth / 8, 3 * constants.pygameWindowHeight / 4))


    @classmethod
    def prepare(cls, self):
        pygame.event.get()
        self.screen.fill((255, 255, 255))


    @classmethod
    def reveal(cls):
        pygame.display.update()
