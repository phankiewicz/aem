import argparse
import os

import numpy as np
from export import export_similarities
from local_search import local_search_greedy, swap_edges, swap_edges_diff
from run import create_distance_matrix, import_vertices_coordinates
from scipy.stats import pearsonr
from texttable import Texttable
from tqdm import tqdm
from visualization import visualize_similarity


def common_vertices(solution1, solution2):

    vertex_sum = 0
    for vertex in solution1[:-1]:
        if vertex in solution2:
            vertex_sum += 1

    return vertex_sum / len(solution1[:-1])


def common_edges(solution1, solution2):

    edges_sum = 0
    for index, vertex in enumerate(solution1[:-1]):
        if vertex in solution2:
            solution2_index = solution2.index(vertex)
            if solution1[index + 1] == solution2[solution2_index + 1]:
                edges_sum += 1

    return edges_sum / (len(solution1) - 1)


def get_similarity_functions_dict():
    return {'edges': common_edges, 'vertices': common_vertices}


def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_files',
        nargs='+',
        type=open,
        help='Specify list of input files\' paths',
    )
    parser.add_argument(
        '--iterations_number', default=1, type=int, help='Specify number of iterations '
    )
    parser.add_argument('--visualize', action='store_true')
    parser.add_argument(
        '--similarity_function',
        choices=get_similarity_functions_dict().keys(),
        required=True,
        help='Specify similarity to be used',
    )
    return parser


def run():
    args = get_argument_parser().parse_args()

    similarity_function = get_similarity_functions_dict()[args.similarity_function]

    min_charts_data = []
    mean_charts_data = []

    table = Texttable()
    table.header(['Name', 'Type', 'Correlation'])

    for input_file in args.input_files:
        instance_name = os.path.basename(input_file.name)
        vertices_coordinates = import_vertices_coordinates(input_file)
        distance_matrix = create_distance_matrix(vertices_coordinates)

        solutions = []
        min_solution = []
        min_cost = 1_000_000

        for _ in tqdm(range(args.iterations_number)):
            solution, cost = local_search_greedy(
                distance_matrix, swap_function=swap_edges, diff_function=swap_edges_diff
            )
            solutions.append((solution, cost))
            if cost < min_cost:
                min_solution = solution
                min_cost = cost

        min_similarities = []
        mean_similarities = []
        for solution, cost in solutions:
            min_similarity = similarity_function(solution, min_solution)
            similarities = [
                similarity_function(solution, other_solution)
                for other_solution, _ in solutions
                if other_solution != solution
            ]
            mean_similarity = sum(similarities) / len(similarities)
            if solution != min_solution:
                min_similarities.append((cost, min_similarity))
            mean_similarities.append((cost, mean_similarity))

        min_charts_data.append(min_similarities)
        export_similarities(
            f'{args.similarity_function}_min_{instance_name}', min_similarities
        )
        X, Y = np.array(min_similarities).T
        correlation, _ = pearsonr(X, Y)
        table.add_row([instance_name, 'min', correlation])

        mean_charts_data.append(mean_similarities)
        export_similarities(
            f'{args.similarity_function}_mean_{instance_name}', mean_similarities
        )
        X, Y = np.array(mean_similarities).T
        correlation, _ = pearsonr(X, Y)
        table.add_row([instance_name, 'mean', correlation])

    print(table.draw())
    if args.visualize:
        for min_chart_data, mean_chart_data in zip(min_charts_data, mean_charts_data):
            visualize_similarity(min_chart_data)
            visualize_similarity(mean_chart_data)


if __name__ == "__main__":
    run()
