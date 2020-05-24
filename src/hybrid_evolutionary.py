import random
import time

from local_search import local_search_steepest, swap_edges, swap_edges_diff
from simple_perturbation_local_search import perturbate_solution


def crossover(parent1, parent2):
    return parent1


def recombination(parent1, parent2):
    for vertex in parent1:


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
    recombination([1, 2, 3, 4, 5, 6, 7, 1], [2, 3, 4, 9, 11, 19, 5, 2])
