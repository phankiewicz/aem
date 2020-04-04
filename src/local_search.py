import random

import math
from collections import defaultdict
import itertools

import numpy as np


def calculate_cycle_length(cycle_vertices, distance_matrix):
    return sum([
        distance_matrix[vertex1, vertex2]
        for vertex1, vertex2 in zip(cycle_vertices, cycle_vertices[1:])
    ])


def swap_edges_diff(distance_matrix, solution, index1, index2):
    edge1_start, edge1_end = solution[index1], solution[(index1 + 1) % len(solution)]
    edge2_start, edge2_end = solution[index2], solution[(index2 + 1) % len(solution)]

    return (
        distance_matrix[edge1_start, edge2_start]
        + distance_matrix[edge1_end, edge2_end]
        - distance_matrix[edge1_start, edge1_end]
        - distance_matrix[edge2_start, edge2_end]
    )


def local_search_greedy(distance_matrix):
    _, matrix_width = distance_matrix.shape
    number_of_vertices_required = math.ceil(0.5 * matrix_width)

    vertices = list(range(matrix_width))

    solution = random.sample(vertices, number_of_vertices_required)

    improvement = True

    while improvement:
        improvement = False

        best_diff = 0
        best_swap = []
        combinations = list(itertools.combinations(
            range(len(solution)), 2
        ))

        for swap_index1, swap_index2 in random.sample(combinations, len(combinations)):
            diff = swap_edges_diff(
                distance_matrix, solution, swap_index1, swap_index2
            )

            if diff < best_diff:
                best_diff = diff
                best_swap = [swap_index1, swap_index2]
                improvement = True

        if improvement:
            swap_index1, swap_index2 = best_swap
            solution = (
                solution[:swap_index1+1]
                + list(reversed(solution[swap_index1+1: swap_index2+1]))
                + solution[swap_index2+1:]
            )

    solution.append(solution[0])
    return solution, calculate_cycle_length(solution, distance_matrix)
