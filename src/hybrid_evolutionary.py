import random
import time

from local_search import local_search_steepest, swap_edges, swap_edges_diff
from simple_perturbation_local_search import perturbate_solution


def crossover(parent1, parent2):
    same_elements = []

    solution1 = parent1[:-1]
    solution2 = parent2[:-1]

    solution1_index = 0

    while solution1_index < len(solution1):
        begin_index = solution1_index
        try:
            solution2_index = solution2.index(solution1[solution1_index])
            while solution1[solution1_index] == solution2[solution2_index]:
                solution1_index += 1
                if(solution1_index >= len(solution1)):
                    break
                solution2_index += 1
                if(solution2_index >= len(solution2)):
                    solution2_index = 0
            end_index = solution1_index
            same_elements.append(solution1[begin_index: end_index])
        except ValueError:
            solution1_index += 1

    total_length = 0

    random_solution = random.choice([solution1, solution2])

    for elem in same_elements:
        total_length += len(elem)
        for vertex in elem:
            random_solution.remove(vertex)

    for vertex in random_solution:
        same_elements.insert(random.randint(0, len(same_elements) - 1), [vertex])

    child = []

    for elem in same_elements:
        for vertex in elem:
            child.append(vertex)

    child.append(child[0])

    return child


def steady_state(distance_matrix, *, iteration_time, population_size, **kwargs):
    initialization_start_time = time.time()
    population = []
    for _ in range(population_size):
        population.append(
            local_search_steepest(
                distance_matrix, swap_function=swap_edges, diff_function=swap_edges_diff
            )
        )
    initialization_time = time.time() - initialization_start_time
    operations_time = iteration_time - initialization_time
    counter = 0
    start_time = time.time()
    while time.time() - start_time < operations_time:
        counter += 1
        if counter % 20 == 0:
            print(time.time() - start_time)

        (parent1, _), (parent2, _) = random.sample(population, 2)
        child_solution = crossover(parent1, parent2)
        child_solution = perturbate_solution(child_solution, distance_matrix)

        child_solution, child_length = child = local_search_steepest(
            distance_matrix,
            swap_function=swap_edges,
            diff_function=swap_edges_diff,
            initial_solution=child_solution,
        )

        in_population = False
        for solution, length in population:
            if (
                len(set(solution).intersection(set(child_solution)))
                == len(set(child_solution))
                and child_length == length
            ):
                in_population = True
                break

        if not in_population:
            max_solution, max_length = max_in_population = max(
                population, key=lambda item: item[1]
            )
            if child_length < max_length:
                population.remove(max_in_population)
                population.append(child)

    min_solution, min_length = min(population, key=lambda item: item[1])
    return min_solution, min_length, counter


if __name__ == "__main__":
    crossover([1, 2, 3, 4, 5, 6, 7, 8, 1], [2, 3, 4, 9, 11, 19, 5, 1, 2])

    crossover([1, 2, 3, 4], [1, 2, 3, 4])

    A = [1, 2, 3, 4, 5]
