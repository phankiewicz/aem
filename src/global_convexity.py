

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
            if(solution1[index + 1] == solution2[solution2_index + 1]):
                edges_sum += 1

    return edges_sum / (len(solution1) - 1)


if __name__ == "__main__":
    print(common_vertices([1, 2, 3, 4, 5, 6, 22, 1], [6, 7, 8, 2, 3, 45, 22, 6]))

    print(common_edges([1, 2, 3, 4, 5, 6, 22, 1], [6, 7, 8, 2, 3, 45, 22, 6]))
