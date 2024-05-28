import math
from functools import reduce


# Функция для расчета площади круга
def circle_area(radius):
    return math.pi * radius ** 2


# Функция для расчета площади прямоугольника
def rectangle_area(width, height):
    return width * height


# Функция для расчета площади фигуры
def calculate_area(shape):
    shape_type = shape[0]
    if shape_type == 'circle':
        return circle_area(shape[1])
    elif shape_type == 'rectangle':
        return rectangle_area(shape[1], shape[2])
    else:
        raise ValueError(f"Unknown shape type: {shape_type}")


# Список фигур, где каждая фигура представлена кортежем
# (тип фигуры, параметры)
shapes = [
    ('circle', 5),
    ('rectangle', 3, 4),
    ('circle', 2),
    ('rectangle', 6, 7)
]

# Вычисление площадей всех фигур
areas = list(map(calculate_area, shapes))


# Суммирование площадей всех фигур
total_area = reduce(lambda x, y: x + y, areas)

print("Площади фигур:", areas)
print("Общая площадь:", total_area)
