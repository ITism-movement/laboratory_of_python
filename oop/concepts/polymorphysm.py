from oop.concepts.inheritance import Shape


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


class Package:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

    def calculate_area(self):
        # Площадь поверхности прямоугольной коробки
        return 2 * (self.length * self.width + self.width * self.height + self.height * self.length)


l = [Rectangle(1, 2), Package(1, 2, 3)]
for el in l:
    print(el.calculate_area())
