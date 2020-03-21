from decimal import ROUND_HALF_UP, Decimal
from math import hypot

import numpy as np


def round_to_integer_mathematically(value):
    return Decimal(str(value)).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)


def import_vertices_coordinates(file_wrapper):
    with file_wrapper as f:
        vertices_coordinates = []
        for index, line in enumerate(f):
            if index >= 7 and not line.startswith('EOF'):
                _, vertex_x, vertex_y = line.split()
                vertices_coordinates.append((int(vertex_x), int(vertex_y)))
    return vertices_coordinates


def create_distance_matrix(vertices_coordinates):
    size = len(vertices_coordinates)
    matrix = np.zeros((size, size))

    for first_index, (first_vertex_x, first_vertex_y) in enumerate(
        vertices_coordinates
    ):
        for second_index, (second_vertex_x, second_vertex_y) in enumerate(
            vertices_coordinates[first_index + 1 :]
        ):
            second_index = second_index + first_index + 1
            distance = hypot(
                first_vertex_x - second_vertex_x, first_vertex_y - second_vertex_y
            )
            matrix[first_index, second_index] = round_to_integer_mathematically(
                distance
            )
            matrix[second_index, first_index] = round_to_integer_mathematically(
                distance
            )
    return matrix


def import_distance_matrix(file_wrapper):
    vertices_coordinates = import_vertices_coordinates(file_wrapper)
    return create_distance_matrix(vertices_coordinates)
