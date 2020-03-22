import argparse
import math
import os

from greedy import greedy_cycle_tsp, nn_greedy_tsp
from importer import create_distance_matrix, import_vertices_coordinates
from texttable import Texttable
from tqdm import tqdm
from visualization import visualize_cycle_and_vertices


def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_files',
        nargs='+',
        type=open,
        help='Specify list of input files\' paths',
    )
    parser.add_argument('--visualize', action='store_true')
    return parser


def run_nn_gready_tsp(distance_matrix, vertices_coordinates):
    results = []
    for index, _ in enumerate(tqdm(vertices_coordinates)):
        cycle_vertices, cycle_length = nn_greedy_tsp(distance_matrix, index)
        assert cycle_vertices[0] == cycle_vertices[-1]
        assert len(cycle_vertices) - 1 == len(set(cycle_vertices))
        _, distance_matrix_width = distance_matrix.shape
        assert len(cycle_vertices) - 1 == math.ceil(0.5 * distance_matrix_width)
        results.append((cycle_vertices, cycle_length))
    return results


def run_greedy_cycle_tsp(distance_matrix, vertices_coordinates):
    results = []
    for index, _ in enumerate(tqdm(vertices_coordinates)):
        cycle_vertices, cycle_length = greedy_cycle_tsp(distance_matrix, index)
        assert cycle_vertices[0] == cycle_vertices[-1]
        assert len(cycle_vertices) - 1 == len(set(cycle_vertices))
        _, distance_matrix_width = distance_matrix.shape
        assert len(cycle_vertices) - 1 == math.ceil(0.5 * distance_matrix_width)
        results.append((cycle_vertices, cycle_length))
    return results


def run():
    args = get_argument_parser().parse_args()

    table = Texttable()
    table.header(['Name', 'Min', 'Average', 'Max'])
    for input_file in args.input_files:
        instance_name = os.path.basename(input_file.name)
        print(instance_name)
        vertices_coordinates = import_vertices_coordinates(input_file)
        distance_matrix = create_distance_matrix(vertices_coordinates)
        results = run_greedy_cycle_tsp(distance_matrix, vertices_coordinates)

        best_cycle, min_length = min(results, key=lambda x: x[1])
        average = sum([length for _, length in results]) / len(results)
        _, max_length = max(results, key=lambda x: x[1])
        table.add_row([instance_name, min_length, average, max_length])
        if args.visualize:
            visualize_cycle_and_vertices(best_cycle, vertices_coordinates)
    print(table.draw())


if __name__ == '__main__':
    run()