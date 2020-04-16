import math


def check_solution_correctness(cycle_vertices, distance_matrix):
    assert cycle_vertices[0] == cycle_vertices[-1]
    assert len(cycle_vertices) - 1 == len(set(cycle_vertices))
    _, distance_matrix_width = distance_matrix.shape
    assert len(cycle_vertices) - 1 == math.ceil(0.5 * distance_matrix_width)
