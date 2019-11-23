import constants
import utility
import abc
import random
import settable
import math
import graphics


class GameObject:
    __metaclass__ = abc.ABCMeta

    def __init__(self, position, max_vel, max_ang_vel, max_radius, color, thickness, collidable=True):
        self.heading = 0
        self.position = position
        self.max_velocity = max_vel
        self.max_angular_velocity = max_ang_vel
        self.velocity = {
            "x-component": 0.,
            "y-component": 0.
        }
        self.angular_velocity = 0
        self.headings_to_vertices = []  # list of tuples: (heading, distance)
        self.health = 100
        self.color = color
        self.thickness = thickness
        self.max_radius = max_radius
        self.collide_radius = 0
        self.non_collide = not collidable

    def get_velocity(self):
        return self.velocity

    def get_angular_velocity(self):
        return self.angular_velocity

    def get_health(self):
        return self.health

    def get_radius(self):
        return self.collide_radius

    def can_collide(self):
        return not self.non_collide

    def set_velocity(self, heading, magnitude):
        heading = heading % constants.CIRCLE_DEG
        magnitude = min([magnitude, self.max_velocity])
        new_vel = utility.get_vector(heading, magnitude)
        self.velocity["x-component"] = new_vel[0]
        self.velocity["y-component"] = new_vel[1]

    def normalize_velocity(self, new_vel):
        new_heading = math.degrees(math.atan(new_vel[1] / new_vel[0]))
        new_magnitude = new_vel[0] / math.cos(math.radians(new_heading))
        self.set_velocity(new_heading, new_magnitude)

    def get_point_from_vertex(self, vertex):
        heading_to_point = (self.heading + vertex[0]) % constants.CIRCLE_DEG
        x_val = self.position[0] + (vertex[1] * math.cos(math.radians(heading_to_point)))
        y_val = self.position[1] + (vertex[1] * math.sin(math.radians(heading_to_point)))
        return x_val, y_val

    @abc.abstractmethod
    def update(self, player_vel=None):
        return NotImplemented

    @abc.abstractmethod
    def draw_self_to_layer(self, graphic_engine, layer):
        return NotImplemented


class Player(GameObject):
    def __init__(self):
        GameObject.__init__(self, [0, 0], constants.PLAYER_MAX_VEL, constants.PLAYER_MAX_ANG_VEL,
                            constants.PLAYER_MAX_RADIUS, settable.PLAYER_COLOR, constants.PLAYER_THICKNESS)
        self.acceleration = constants.PLAYER_ACCELERATION
        self.angular_acceleration = constants.PLAYER_ANGULAR_ACCELERATION
        self.headings_to_vertices = [(0, constants.PLAYER_MAX_RADIUS),
                                     (140, constants.PLAYER_MAX_RADIUS),
                                     (180, constants.PLAYER_MAX_RADIUS / 3),
                                     (220, constants.PLAYER_MAX_RADIUS)]

    def thrust(self):
        new_vel = utility.vector_add((self.velocity["x-component"], self.velocity["y-component"]),
                                     utility.get_vector(self.heading, self.acceleration))
        self.normalize_velocity(new_vel)

    def turn(self, direction):
        if direction == "right":
            self.angular_velocity = min([self.max_angular_velocity, self.angular_velocity + self.angular_acceleration])
        elif direction == "left":
            self.angular_velocity = max([-self.max_angular_velocity, self.angular_velocity - self.angular_acceleration])
        else:
            raise NotImplementedError

    def update(self, player_vel=None):
        self.heading = (self.heading + self.angular_velocity) % constants.CIRCLE_DEG

    def draw_self_to_layer(self, graphic_engine, layer):
        for vertex in self.headings_to_vertices:
            graphic_engine.add_to_layer(layer,
                                        graphics.Line(self.get_point_from_vertex(vertex),  # Line.start
                                                      self.get_point_from_vertex(utility.get_next(vertex, self.headings_to_vertices)),  # Line.end
                                                      self.color, self.thickness))  # Line.color, Line.thickness)

    def brake(self):
        if self.angular_velocity < 0:
            self.angular_velocity += self.angular_acceleration
            if self.angular_velocity > 0:
                self.angular_velocity = 0
        elif self.angular_velocity > 0:
            self.angular_velocity -= self.angular_acceleration
            if self.angular_velocity < 0:
                self.angular_velocity = 0


class Asteroid(GameObject):
    def __init__(self, position, velocity, ang_vel):
        GameObject.__init__(self, position, constants.ASTEROID_MAX_VEL, constants.ASTEROID_MAX_ANG_VEL,
                            constants.ASTEROID_MAX_RADIUS, settable.ASTEROID_COLOR, constants.ASTEROID_THICKNESS)
        self.velocity["x-component"] = velocity[0]
        self.velocity["y-component"] = velocity[1]
        self.angular_velocity = min([ang_vel, self.max_angular_velocity])
        self.has_built = False
        self.build_asteroid()

    def build_asteroid(self):
        if not self.has_built:
            num_vertices = random.randint(constants.ASTEROID_MIN_VERTICES, constants.ASTEROID_MAX_VERTICES)
            separation_angle = constants.CIRCLE_DEG / num_vertices
            for v in range(num_vertices):
                vertex_heading = random.randint(math.floor(separation_angle * v - separation_angle * 0.25),
                                                math.ceil(separation_angle * v + separation_angle * 0.25))
                vertex_radius = random.randint(constants.ASTEROID_MIN_RADIUS, self.max_radius)
                self.headings_to_vertices.append((vertex_heading, vertex_radius))
        self.has_built = True

    def update(self, player_vel=None):
        self.heading = (self.heading + self.angular_velocity) % constants.CIRCLE_DEG
        self.position[0] = self.position[0] + self.velocity["x-component"] - player_vel["x-component"]
        self.position[1] = self.position[1] + self.velocity["y-component"] - player_vel["y-component"]

    def draw_self_to_layer(self, graphic_engine, layer):
        for vertex in self.headings_to_vertices:
            graphic_engine.add_to_layer(layer,
                                        graphics.Line(self.get_point_from_vertex(vertex),  # Line.start
                                                      self.get_point_from_vertex(utility.get_next(vertex, self.headings_to_vertices)),  # Line.end
                                                      self.color, self.thickness))  # Line.color, Line.thickness)


class Bullet(GameObject):
    def __init__(self):
        GameObject.__init__(self)


class Snow(GameObject):
    def __init__(self):
        GameObject.__init__(self)
