import math
from collections import defaultdict

import numpy as np

def swap_outer_verices(cycle_vertices, other_vertices):
    pass

def swap_inner_vertices(cycle_vertices):
    pass

def swap_edges(cycle_vertices):
    pass

def local_greedy_tsp(distance_matrix, starting_vertex):
    _, matrix_width = distance_matrix.shape
    number_of_vertices_required = math.ceil(0.5 * matrix_width)
    vertices_visited = np.zeros(matrix_width)
    cycle_vertices = []
    cycle_length = 0

    return cycle_vertices, cycle_length
