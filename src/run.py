import argparse
import os
import time

from greedy import greedy_cycle_tsp, nn_greedy_tsp, regret_1_greedy_cycle_tsp
from importer import create_distance_matrix, import_vertices_coordinates
from local_search import (
    local_search_greedy,
    local_search_steepest,
    swap_edges,
    swap_edges_diff,
    swap_vertices,
    swap_vertices_diff,
)
from simple_perturbation_local_search import simple_perturbation_local_search
from texttable import Texttable
from tqdm import tqdm
from utils import check_solution_correctness
from visualization import visualize_cycle_and_vertices


def get_argument_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Heuristics types', dest='type')
    constructive_parser = subparsers.add_parser('constructive')
    constructive_parser.add_argument(
        '--algorithm',
        choices=get_constructive_algorithms_dict().keys(),
        required=True,
        help='Specify algorithm to be used',
    )
    local_search_parser = subparsers.add_parser('local_search')
    local_search_parser.add_argument(
        '--algorithm',
        choices=get_local_search_algorithms_dict().keys(),
        required=True,
        help='Specify algorithm to be used',
    )
    local_search_parser.add_argument(
        '--neighbourhood',
        choices=get_local_search_neighbourhood_dict().keys(),
        required=True,
        help='Specify neighbourhood to be used',
    )
    local_search_parser.add_argument(
        '--multiple_start_number',
        default=1,
        type=int,
        help='Specify number of iterations in multiple start',
    )

    for subparser in [constructive_parser, local_search_parser]:
        subparser.add_argument(
            '--input_files',
            nargs='+',
            type=open,
            help='Specify list of input files\' paths',
        )
        subparser.add_argument('--visualize', action='store_true')
    return parser


def run_nn_gready_tsp(distance_matrix, vertices_coordinates, *args, **kwargs):
    results = []
    for index, _ in enumerate(tqdm(vertices_coordinates)):
        start_time = time.time()
        cycle_vertices, cycle_length = nn_greedy_tsp(distance_matrix, index)
        check_solution_correctness(cycle_vertices, distance_matrix)
        results.append((cycle_vertices, cycle_length, time.time() - start_time))
    return results


def run_greedy_cycle_tsp(distance_matrix, vertices_coordinates, *args, **kwargs):
    results = []
    for index, _ in enumerate(tqdm(vertices_coordinates)):
        start_time = time.time()
        cycle_vertices, cycle_length = greedy_cycle_tsp(distance_matrix, index)
        check_solution_correctness(cycle_vertices, distance_matrix)
        results.append((cycle_vertices, cycle_length, time.time() - start_time))
    return results


def run_regret_1_greedy_cycle_tsp(
    distance_matrix, vertices_coordinates, *args, **kwargs
):
    results = []
    for index, _ in enumerate(tqdm(vertices_coordinates)):
        start_time = time.time()
        cycle_vertices, cycle_length = regret_1_greedy_cycle_tsp(distance_matrix, index)
        check_solution_correctness(cycle_vertices, distance_matrix)
        results.append((cycle_vertices, cycle_length, time.time() - start_time))
    return results


def run_local_search_greedy(
    distance_matrix, vertices_coordinates, *, multiple_start_number, **kwargs
):
    results = []
    for _ in tqdm(vertices_coordinates):
        inner_results = []
        start_time = time.time()
        for _ in range(multiple_start_number):
            cycle_vertices, cycle_length = local_search_greedy(
                distance_matrix, **kwargs
            )
            check_solution_correctness(cycle_vertices, distance_matrix)
            inner_results.append((cycle_vertices, cycle_length))
        min_cycle_vertices, min_cycle_length, = min(inner_results, key=lambda x: x[1])
        results.append((min_cycle_vertices, min_cycle_length, time.time() - start_time))
    return results


def run_local_search_steepest(
    distance_matrix, vertices_coordinates, *, multiple_start_number, **kwargs
):
    results = []
    for _ in tqdm(vertices_coordinates):
        inner_results = []
        start_time = time.time()
        for _ in range(multiple_start_number):
            cycle_vertices, cycle_length = local_search_steepest(
                distance_matrix, **kwargs
            )
            check_solution_correctness(cycle_vertices, distance_matrix)
            inner_results.append((cycle_vertices, cycle_length))
        min_cycle_vertices, min_cycle_length, = min(inner_results, key=lambda x: x[1])
        results.append((cycle_vertices, cycle_length, time.time() - start_time))
    return results


def run_simple_perturbance_local_search(
    distance_matrix, vertices_coordinates, *, multiple_start_number, **kwargs
):
    results = []
    for _ in tqdm(range(10)):
        inner_results = []
        start_time = time.time()
        for _ in range(multiple_start_number):
            cycle_vertices, cycle_length = simple_perturbation_local_search(
                distance_matrix, **kwargs
            )
            check_solution_correctness(cycle_vertices, distance_matrix)
            inner_results.append((cycle_vertices, cycle_length))
        min_cycle_vertices, min_cycle_length, = min(inner_results, key=lambda x: x[1])
        results.append((cycle_vertices, cycle_length, time.time() - start_time))
    return results


def get_local_search_neighbourhood_dict():
    return {
        'vertices': {
            'swap_function': swap_vertices,
            'diff_function': swap_vertices_diff,
        },
        'edges': {'swap_function': swap_edges, 'diff_function': swap_edges_diff},
    }


def get_local_search_extra_kwargs(run_args):
    extra_kwargs = {'multiple_start_number': run_args.multiple_start_number}
    neighbourhood_kwargs = get_local_search_neighbourhood_dict()[run_args.neighbourhood]
    extra_kwargs.update(neighbourhood_kwargs)
    return extra_kwargs


def get_local_search_algorithms_dict():
    return {
        'greedy': run_local_search_greedy,
        'steepest': run_local_search_steepest,
        'simple_perturbation': run_simple_perturbance_local_search,
    }


def get_constructive_algorithms_dict():
    return {
        'nn_greedy': run_nn_gready_tsp,
        'greedy_cycle': run_greedy_cycle_tsp,
        'regret_1_greedy_cycle': run_regret_1_greedy_cycle_tsp,
    }


def get_algorithms_dict():
    return {
        'constructive': get_constructive_algorithms_dict(),
        'local_search': get_local_search_algorithms_dict(),
    }


def run():
    args = get_argument_parser().parse_args()

    table = Texttable()
    table.header(
        [
            'Name',
            'Min length',
            'Average length',
            'Max length',
            'Min time [s]',
            'Average time [s]',
            'Max time [s]',
        ]
    )
    solutions = []
    for input_file in args.input_files:
        instance_name = os.path.basename(input_file.name)
        print(instance_name)
        vertices_coordinates = import_vertices_coordinates(input_file)
        distance_matrix = create_distance_matrix(vertices_coordinates)
        algorithms_dict = get_algorithms_dict()[args.type]
        run_function = algorithms_dict[args.algorithm]

        extra_kwargs = (
            get_local_search_extra_kwargs(args) if args.type == 'local_search' else {}
        )
        results = run_function(distance_matrix, vertices_coordinates, **extra_kwargs)

        best_cycle, min_length, _ = min(results, key=lambda x: x[1])
        average = sum([length for _, length, _ in results]) / len(results)
        _, max_length, _ = max(results, key=lambda x: x[1])

        _, _, min_time = min(results, key=lambda x: x[2])
        average_time = sum([time for _, _, time in results]) / len(results)
        _, _, max_time = max(results, key=lambda x: x[2])

        table.add_row(
            [
                instance_name,
                min_length,
                average,
                max_length,
                min_time,
                average_time,
                max_time,
            ]
        )
        solutions.append((best_cycle, vertices_coordinates))
    print(table.draw())
    if args.visualize:
        for solution in solutions:
            best_cycle, vertices_coordinates = solution
            visualize_cycle_and_vertices(best_cycle, vertices_coordinates)


if __name__ == '__main__':
    run()
