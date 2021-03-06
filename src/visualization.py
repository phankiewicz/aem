import matplotlib.pyplot as plt


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
