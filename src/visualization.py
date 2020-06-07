import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np


def visualize_cycle_and_vertices(cycle, vertices_coordinates):
    for index, _ in enumerate(cycle[:-1]):
        first_item_index = cycle[index]
        second_item_index = cycle[index + 1]
        first_point_x, first_point_y = vertices_coordinates[first_item_index]
        second_point_x, second_point_y = vertices_coordinates[second_item_index]
        plt.plot([first_point_x, second_point_x], [first_point_y, second_point_y], 'k-')
    for x, y in vertices_coordinates:
        plt.plot(x, y, 'ro')
    plt.show()


def visualize_similarity(chart_data):
    X, Y = np.array(chart_data).T
    correlation, _ = pearsonr(X, Y)
    for x, y in chart_data:
        plt.plot(x, y, 'ro')
    plt.title("correlation:" + str(correlation))
    plt.show()
