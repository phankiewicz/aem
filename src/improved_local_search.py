import itertools
import math
import random

from local_search import calculate_cycle_length, swap_outer_vertices_diff
from sortedcontainers import SortedList


def remove_vertex_from_moves_list(improving_moves_list, vertices):
    items_to_remove = list()
    for item in improving_moves_list:
        (vertex1, vertex2), diff = item
        if vertex1 in vertices or vertex2 in vertices:
            items_to_remove.append(item)
    for item in items_to_remove:
        improving_moves_list.remove(item)


def moves_list_local_search_steepest(
    distance_matrix, swap_function, diff_function, *args, **kwargs
):
    _, matrix_width = distance_matrix.shape
    number_of_vertices_required = math.ceil(0.5 * matrix_width)

    vertices = list(range(matrix_width))

    improving_moves_list = SortedList(key=lambda x: x[1])
    checked_moves = {}

    solution = random.sample(vertices, number_of_vertices_required)

    improvement = True

    while improvement:
        improvement = False
        outer_improvement = False

        solution_indexes = {item: index for index, item in enumerate(solution)}

        combinations = list(itertools.combinations(range(len(solution)), 2))
        filtered_combinations = list(
            filter(lambda x: abs(x[0] - x[1]) != 1, combinations)
        )

        not_checked_combinations = [
            (index1, index2)
            for index1, index2 in filtered_combinations
            if checked_moves.get((solution[index1], solution[index2])) is None
        ]

        for swap_index1, swap_index2 in random.sample(
            not_checked_combinations, len(not_checked_combinations)
        ):
            diff = diff_function(distance_matrix, solution, swap_index1, swap_index2)

            if diff < 0:
                improving_moves_list.add(
                    ((solution[swap_index1], solution[swap_index2]), diff)
                )

        other_vertices = [i for i in range(0, matrix_width) if i not in solution]
        outer_combinations = list(
            itertools.product(range(len(solution)), other_vertices)
        )

        for old_vertex_index, new_vertex in random.sample(
            outer_combinations, len(outer_combinations)
        ):

            diff = swap_outer_vertices_diff(
                distance_matrix, solution, old_vertex_index, new_vertex
            )
            # if diff < 0:
            #     improving_moves_list.add(
            #         ((solution[old_vertex_index], new_vertex), diff)
            #     )

        to_be_removed = []
        for item in improving_moves_list:
            (vertex1, vertex2), diff = item
            assert diff < 0
            assert vertex1 in solution and vertex2 in solution
            if vertex1 in solution:
                improvement = True
                if vertex2 not in solution:
                    outer_improvement = True
                    best_swap = [solution_indexes[vertex1], vertex2]
                else:
                    outer_improvement = False
                    best_move = vertex1, vertex2
                    best_swap = [solution_indexes[vertex1], solution_indexes[vertex2]]
                break

            to_be_removed.append(item)

        checked_moves.update({indexes: diff for indexes, diff in improving_moves_list})

        # print(len(checked_moves))

        # print(len(to_be_removed))
        # print(to_be_removed)
        # print(best_diff)

        # previous_improving_moves_list_length = len(improving_moves_list)
        # print(previous_improving_moves_list_length)
        # print(to_be_removed)
        for item in to_be_removed:
            improving_moves_list.remove(item)

        remove_vertex_from_moves_list(improving_moves_list, best_move)

        # print(len(improving_moves_list))
        assert not outer_improvement
        if improvement:
            if outer_improvement:
                old_vertex_index, new_vertex = best_swap
                solution[old_vertex_index] = new_vertex
            else:
                swap_index1, swap_index2 = best_swap
                if swap_index1 > swap_index2:
                    swap_index1, swap_index2 = swap_index2, swap_index1
                solution = swap_function(solution, swap_index1, swap_index2)

    solution.append(solution[0])
    return solution, calculate_cycle_length(solution, distance_matrix)
