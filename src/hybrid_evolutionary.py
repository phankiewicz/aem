import time

from local_search import local_search_steepest, swap_edges, swap_edges_diff


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
        # steady_state code here

    min_solution, min_length = min(population, key=lambda item: item[1])
    return min_solution, min_length, counter


if __name__ == "__main__":
    recombination([1, 2, 3, 4, 5, 6, 7, 1], [2, 3, 4, 9, 11, 19, 5, 2])
