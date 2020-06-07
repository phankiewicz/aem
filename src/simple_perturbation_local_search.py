import itertools
import random

from local_search import local_search_steepest, swap_edges


def perturbate_solution(
    cycle_solution, distance_matrix, outer_move_count=2, inner_move_count=2
):
    _, matrix_width = distance_matrix.shape
    solution = cycle_solution[:-1]
    for _ in range(outer_move_count):
        other_vertices = [i for i in range(0, matrix_width) if i not in solution]
        outer_index = random.choice(other_vertices)

        old_vertex_index = random.choice(range(len(solution)))
        solution[old_vertex_index] = outer_index

    for _ in range(inner_move_count):
        combinations = list(itertools.combinations(range(len(solution)), 2))
        swap_index1, swap_index2 = random.choice(combinations)
        solution = swap_edges(solution, swap_index1, swap_index2)
    solution.append(solution[0])
    return solution


def simple_perturbation_local_search(distance_matrix, *args, **kwargs):
    min_solution, min_length = local_search_steepest(distance_matrix, *args, **kwargs)

    for _ in range(100):
        perturbated_solution = perturbate_solution(min_solution, distance_matrix)
        current_solution, current_length = local_search_steepest(
            distance_matrix, *args, initial_solution=perturbated_solution, **kwargs
        )

        if current_length < min_length:
            min_solution, min_length = current_solution, current_length

    return min_solution, min_length
