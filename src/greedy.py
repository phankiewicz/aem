import math

import numpy as np


def nn_greedy_tsp(distance_matrix, starting_vertex):
    _, matrix_width = distance_matrix.shape
    number_of_vertices_required = math.ceil(0.5 * matrix_width)
    vertices_visited = np.zeros(matrix_width)
    cycle_vertices = []
    cycle_length = 0

    current_vertex = starting_vertex

    for iteration in range(number_of_vertices_required):
        cycle_vertices.append(current_vertex)
        vertices_visited[current_vertex] = 1

        distances = [
            (index, distance)
            for index, distance in enumerate(distance_matrix[current_vertex, :])
            if distance != 0 and not vertices_visited[index]
        ]
        current_vertex, min_distance = min(distances, key=lambda x: x[1])
        cycle_length += min_distance

    last_vertex = current_vertex
    cycle_vertices.append(starting_vertex)
    cycle_length += distance_matrix[starting_vertex, last_vertex]

    return cycle_vertices, cycle_length
