import math
from collections import defaultdict

import numpy as np


def get_regret(insertion_costs):
    if len(insertion_costs) >= 2:
        return insertion_costs[1][0] - insertion_costs[0][0]
    return insertion_costs[0][0] * -1


def nn_greedy_tsp(distance_matrix, starting_vertex, *args, **kwargs):
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


def regret_1_greedy_cycle_tsp(distance_matrix, starting_vertex, *args, **kwargs):
    _, matrix_width = distance_matrix.shape
    number_of_vertices_required = math.ceil(0.5 * matrix_width)
    vertices_visited = np.zeros(matrix_width)
    cycle_vertices = []
    cycle_length = 0

    cycle_vertices.extend([starting_vertex, starting_vertex])
    vertices_visited[starting_vertex] = 1

    for iteration in range(number_of_vertices_required - 1):
        insertion_costs = []
        insertion_costs_per_vertex = defaultdict(list)
        for first_vertex, second_vertex in zip(cycle_vertices, cycle_vertices[1:]):
            for target_vertex in [
                vertex for vertex in range(matrix_width) if not vertices_visited[vertex]
            ]:
                insertion_cost = (
                    distance_matrix[first_vertex, target_vertex]
                    + distance_matrix[second_vertex, target_vertex]
                    - distance_matrix[first_vertex, second_vertex]
                )
                insertion_costs_per_vertex[target_vertex].append(
                    (insertion_cost, target_vertex, (first_vertex, second_vertex))
                )
                insertion_costs.append(
                    (insertion_cost, target_vertex, (first_vertex, second_vertex))
                )

        for key, value in insertion_costs_per_vertex.items():
            insertion_costs_per_vertex[key] = sorted(value, key=lambda x: x[0])

        regrets = [
            (vertex, get_regret(insertion_costs))
            for vertex, insertion_costs in insertion_costs_per_vertex.items()
        ]

        biggest_regret_vertex, _ = max(regrets, key=lambda x: x[1])

        chosen_insertion = insertion_costs_per_vertex[biggest_regret_vertex][0]
        chosen_insertion_cost, chosen_vertex, (
            first_position_vertex,
            second_position_vertex,
        ) = chosen_insertion
        assert chosen_vertex == biggest_regret_vertex
        cycle_length += chosen_insertion_cost
        position_index = cycle_vertices.index(first_position_vertex) + 1
        assert cycle_vertices[position_index] == second_position_vertex
        cycle_vertices.insert(position_index, chosen_vertex)
        vertices_visited[chosen_vertex] = 1

    return cycle_vertices, cycle_length


def greedy_cycle_tsp(distance_matrix, starting_vertex, *args, **kwargs):
    _, matrix_width = distance_matrix.shape
    number_of_vertices_required = math.ceil(0.5 * matrix_width)
    vertices_visited = np.zeros(matrix_width)
    cycle_vertices = []
    cycle_length = 0

    cycle_vertices.extend([starting_vertex, starting_vertex])
    vertices_visited[starting_vertex] = 1

    for iteration in range(number_of_vertices_required - 1):
        insertion_costs = []
        for first_vertex, second_vertex in zip(cycle_vertices, cycle_vertices[1:]):
            for target_vertex in [
                vertex for vertex in range(matrix_width) if not vertices_visited[vertex]
            ]:
                insertion_cost = (
                    distance_matrix[first_vertex, target_vertex]
                    + distance_matrix[second_vertex, target_vertex]
                    - distance_matrix[first_vertex, second_vertex]
                )
                insertion_costs.append(
                    (insertion_cost, target_vertex, (first_vertex, second_vertex))
                )

        min_insertion_cost, new_vertex, (
            first_position_vertex,
            second_position_vertex,
        ) = min(insertion_costs, key=lambda x: x[0])
        cycle_length += min_insertion_cost
        position_index = cycle_vertices.index(first_position_vertex) + 1
        assert cycle_vertices[position_index] == second_position_vertex
        cycle_vertices.insert(position_index, new_vertex)
        vertices_visited[new_vertex] = 1

    return cycle_vertices, cycle_length
