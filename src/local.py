import math
from collections import defaultdict

import numpy as np
import random

def swap_outer_verices(cycle_vertices, old_vertex, new_vertex):
    cycle_vertices[cycle_vertices.index(old_vertex)] = new_vertex

    return cycle_vertices

def swap_inner_vertices(cycle_vertices, first, second):
    first_index = cycle_vertices.index(first)
    second_index = cycle_vertices.index(second)
    cycle_vertices[first_index], cycle_vertices[second_index] = cycle_vertices[second_index], cycle_vertices[first_index]

    return swap_inner_vertices

def swap_edges(cycle_vertices):
    pass

def generate_random_cycle(matrix_width, number_of_vertices_required):
    random_cycle_vertices = random.sample(range(0, matrix_width), number_of_vertices_required)

    random_cycle_vertices.append(random_cycle_vertices[0])
    return random_cycle_vertices

def local_greedy_tsp(distance_matrix, starting_vertex):
    _, matrix_width = distance_matrix.shape
    number_of_vertices_required = math.ceil(0.5 * matrix_width)
    vertices_visited = np.zeros(matrix_width)
    cycle_vertices = []
    cycle_length = 0

    cycle_vertices = generate_random_cycle(matrix_width, number_of_vertices_required)
    other_vertices = [i for i in range(0, matrix_width) if i not in cycle_vertices]


    for current_vertex, next_vertex in zip(cycle_vertices[0:], cycle_vertices[1:]):
        cycle_length += distance_matrix[current_vertex, next_vertex]

    #random search order
    search_order = [i for i in range(0, len(cycle_vertices) - 1)]
    random.shuffle(search_order)

    for first_vertex_to_swap in search_order:
        search_order2 = [i for i in range(0, len(cycle_vertices) - 1)]
        random.shuffle(search_order2)

        delta = cycle_length
        for second_vertex_to_swap in search_order2:
            delta -= distance_matrix[first_vertex_to_swap - 1, first_vertex_to_swap]
            delta -= distance_matrix[first_vertex_to_swap, first_vertex_to_swap + 1]
            delta -= distance_matrix[second_vertex_to_swap - 1, second_vertex_to_swap]
            delta -= distance_matrix[second_vertex_to_swap, second_vertex_to_swap + 1]

            delta += distance_matrix[first_vertex_to_swap - 1, second_vertex_to_swap]






    return cycle_vertices, cycle_length