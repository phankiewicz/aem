import time

from local_search import local_search_steepest, swap_edges, swap_edges_diff


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

    return min(population, key=lambda item: item[1])
