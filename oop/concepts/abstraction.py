from abc import ABC, abstractmethod
import math


class Shape(ABC):
    @abstractmethod
    def calculate_area(self):
        pass

    @abstractmethod
    def calculate_perimeter(self):
        pass


class Triangle(Shape):
    def __init__(self, side1, side2, side3):
        self.__side1 = side1
        self.__side2 = side2
        self.__side3 = side3

    @property
    def side1(self):
        return self.__side1

    @side1.setter
    def side1(self, side1):
        if side1 > 0:
            self.__side1 = side1
        else:
            raise ValueError("Side must be positive")

    @property
    def side2(self):
        return self.__side2

    @side2.setter
    def side2(self, side2):
        if side2 > 0:
            self.__side2 = side2
        else:
            raise ValueError("Side must be positive")

    @property
    def side3(self):
        return self.__side3

    @side3.setter
    def side3(self, side3):
        if side3 > 0:
            self.__side3 = side3
        else:
            raise ValueError("Side must be positive")

    def calculate_area(self):
        s = (self.__side1 + self.__side2 + self.__side3) / 2
        return math.sqrt(s * (s - self.__side1) * (s - self.__side2) * (s - self.__side3))

    def calculate_perimeter(self):
        return self.__side1 + self.__side2 + self.__side3


class Rectangle(Shape):
    def __init__(self, width, height):
        self.__width = width
        self.__height = height

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        if width > 0:
            self.__width = width
        else:
            raise ValueError("Width must be positive")

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        if height > 0:
            self.__height = height
        else:
            raise ValueError("Height must be positive")

    def calculate_area(self):
        return self.__width * self.__height

    def calculate_perimeter(self):
        return 2 * (self.__width + self.__height)
