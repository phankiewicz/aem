import itertools
import random
import numpy as np

from local_search import local_search_steepest, swap_edges



def greedy_repar_tsp(distance_matrix, solution):
    _, matrix_width = distance_matrix.shape

    number_of_vertices_required = len(solution)

    vertices_visited = np.zeros(matrix_width)

    cycle_vertices = []
    for vertex in solution:
        if(vertex != -1):
            vertices_visited[vertex] = 1
            cycle_vertices.append(vertex)

    cycle_vertices.append(cycle_vertices[0])
    
    cycle_length = len(cycle_vertices)

    for iteration in range(number_of_vertices_required - (cycle_length - 1)):
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

    return cycle_vertices

def perturbate_solution(cycle_solution, distance_matrix):
    solution = cycle_solution[:-1]

    #destroy
    num_of_vertices_to_destory = int(len(solution) / 5)

    start_vertex_index = random.choice(range(len(solution)))
    for i in range(num_of_vertices_to_destory):
        if(start_vertex_index + i < len(solution)):
            solution[start_vertex_index + i] = -1
        else:
            solution[(start_vertex_index + i) - len(solution)] = -1
    
    #repair

    solution = greedy_repar_tsp(distance_matrix, solution)

    return solution


def big_perturbation_local_search(distance_matrix, *args, **kwargs):
    min_solution, min_length = local_search_steepest(distance_matrix, *args, **kwargs)

    for _ in range(100):
        perturbated_solution = perturbate_solution(min_solution, distance_matrix)
        current_solution, current_length = local_search_steepest(
            distance_matrix, *args, initial_solution=perturbated_solution, **kwargs
        )

        if current_length < min_length:
            min_solution, min_length = current_solution, current_length

    return min_solution, min_length
