import pygame
from pygame.math import Vector2 as _Vector2 # underscore in front because both libraries have a Vector2 class

from pyray import *

class Rect(pygame.FRect):
    """
    Modified from the original pygame.Rect class to include an export to raylib struct called toray().
    pygame.Rect() contains much more functionality, but we still need to use the raylib Rectangle() struct for raylib functions.
    You can use the .toray() method to return a raylib Rectangle useful for displaying.
    """
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
    def toray(self):
        return Rectangle(self.x, self.y, self.width, self.height)
    def toray_vec2(self):
        return Vector2(self.x, self.y)


class vec2(_Vector2):
    """
    Modified from the original pygame.math.Vector2() class to include an export to raylib struct called toray().
    pygame.math.Vector2() contains much more functionality, but we still need to use the raylib Vector2() struct for raylib functions.
    You can use the .toray() method to return a raylib Vector2 useful for displaying.
    """
    def __init__(self, x, y):
        super().__init__(x, y)
    def toray(self):
        return Vector2(self.x, self.y)