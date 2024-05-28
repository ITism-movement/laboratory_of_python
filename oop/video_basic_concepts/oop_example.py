import math


# Класс для круга
class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2


# Класс для прямоугольника
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


# Создание списка фигур
shapes = [
    Circle(5),
    Rectangle(3, 4),
    Circle(2),
    Rectangle(6, 7)
]

# Вычисление площадей всех фигур
areas = [shape.area() for shape in shapes]

# Суммирование площадей всех фигур
total_area = sum(areas)

print("Площади фигур:", areas)
print("Общая площадь:", total_area)
