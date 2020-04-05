import random

import math
from collections import defaultdict
import itertools

import numpy as np


def calculate_cycle_length(cycle_vertices, distance_matrix):
    return sum([
        distance_matrix[vertex1, vertex2]
        for vertex1, vertex2 in zip(cycle_vertices, cycle_vertices[1:])
    ])

def swap_outer_vertices_diff(distance_matrix, solution, index_old, new_edge_start):
    
    old_edge2_index = index_old - 1
    if(old_edge2_index < 0):
        old_edge2_index = len(solution) - 1

    old_edge_start = solution[index_old]
    old_edge1_end, old_edge2_end = solution[old_edge2_index], solution[(index_old + 1) % len(solution)]

    return (
        distance_matrix[new_edge_start, old_edge1_end]
        + distance_matrix[new_edge_start, old_edge2_end]
        - distance_matrix[old_edge_start, old_edge1_end]
        - distance_matrix[old_edge_start, old_edge2_end]
    )

def swap_edges_diff(distance_matrix, solution, index1, index2):
    edge1_start, edge1_end = solution[index1], solution[(index1 + 1) % len(solution)]
    edge2_start, edge2_end = solution[index2], solution[(index2 + 1) % len(solution)]

    return (
        distance_matrix[edge1_start, edge2_start]
        + distance_matrix[edge1_end, edge2_end]
        - distance_matrix[edge1_start, edge1_end]
        - distance_matrix[edge2_start, edge2_end]
    )

def local_search_greedy_steepest(distance_matrix):
    _, matrix_width = distance_matrix.shape
    number_of_vertices_required = math.ceil(0.5 * matrix_width)

    vertices = list(range(matrix_width))

    solution = random.sample(vertices, number_of_vertices_required)
    

    improvement = True

    while improvement:
        improvement = False
        outer_improvement = False
        best_diff = 0
        best_swap = []
        
        combinations = list(itertools.combinations(
            range(len(solution)), 2
        ))

        for swap_index1, swap_index2 in random.sample(combinations, len(combinations)):
            diff = swap_edges_diff(
                distance_matrix, solution, swap_index1, swap_index2
            )

            if diff < best_diff:
                best_diff = diff
                best_swap = [swap_index1, swap_index2]
                improvement = True
        
        other_vertices = [i for i in range(0, matrix_width) if i not in solution]
        outer_combinations = list(itertools.product(range(len(solution)), other_vertices))

        for old_vertex_index, new_vertex in random.sample(outer_combinations, len(outer_combinations)): 
            
            diff = swap_outer_vertices_diff(
                distance_matrix, solution, old_vertex_index, new_vertex
            )
       
            if diff < best_diff:
                best_diff = diff
                best_swap = [old_vertex_index, new_vertex]
                outer_improvement = True
                improvement = True
         
        if improvement:
            if outer_improvement:
                old_vertex_index, new_vertex = best_swap
                solution[old_vertex_index] = new_vertex
            else:
                swap_index1, swap_index2 = best_swap
                solution = (
                    solution[:swap_index1+1]
                    + list(reversed(solution[swap_index1+1: swap_index2+1]))
                    + solution[swap_index2+1:]
                )


    solution.append(solution[0])
    return solution, calculate_cycle_length(solution, distance_matrix)

def local_search_greedy(distance_matrix):
    _, matrix_width = distance_matrix.shape
    number_of_vertices_required = math.ceil(0.5 * matrix_width)

    vertices = list(range(matrix_width))

    solution = random.sample(vertices, number_of_vertices_required)
    

    improvement = True



    while improvement:
        improvement = False
        outer_improvement = False
        best_diff = 0
        best_swap = []
        
        combinations = list(itertools.combinations(
            range(len(solution)), 2
        ))

        swap_type = True       

        inner_swap = random.sample(combinations, len(combinations))
        inner_next_id = 0

        other_vertices = [i for i in range(0, matrix_width) if i not in solution]
        outer_combinations = list(itertools.product(range(len(solution)), other_vertices))

        outer_swap = random.sample(outer_combinations, len(outer_combinations))
        outer_next_id = 0

        for _ in range(len(inner_swap) + len(outer_swap) - 1):
            if(swap_type):
                try:
                    swap_index1, swap_index2 = inner_swap[inner_next_id]
                except:
                    pass
                diff = swap_edges_diff(
                    distance_matrix, solution, swap_index1, swap_index2
                )

                if diff < best_diff:
                    best_diff = diff
                    best_swap = [swap_index1, swap_index2]
                    improvement = True
                    break

                swap_type = not swap_type
                inner_next_id += 1

            else:
                old_vertex_index, new_vertex = outer_swap[outer_next_id]
                
                diff = swap_outer_vertices_diff(
                    distance_matrix, solution, old_vertex_index, new_vertex
                )
        
                if diff < best_diff:
                    best_diff = diff
                    best_swap = [old_vertex_index, new_vertex]
                    outer_improvement = True
                    improvement = True
                    break

                swap_type = not swap_type
                outer_next_id += 1
         
        if improvement:
            if outer_improvement:
                old_vertex_index, new_vertex = best_swap
                solution[old_vertex_index] = new_vertex
            else:
                swap_index1, swap_index2 = best_swap
                solution = (
                    solution[:swap_index1+1]
                    + list(reversed(solution[swap_index1+1: swap_index2+1]))
                    + solution[swap_index2+1:]
                )


    solution.append(solution[0])
    return solution, calculate_cycle_length(solution, distance_matrix)
