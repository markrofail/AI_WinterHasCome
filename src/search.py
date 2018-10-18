import functools
import itertools
import operator
import sys
import numpy as np

from src.models.node import Node


def print_debug(node):
    state = node.state
    print('D:', state.dragon_glass(), 'W:', state.white_walkers(), state.grid)


def general_search(problem, queueing_function):
    nodes = [Node(problem.initial_state)]
    visited = list()
    count = 0
    while nodes:
        node = nodes.pop(0)  # remove front
        visited.append(node)
        if problem.goal_test(node.state):
            return node, count
        nodes = queueing_function(nodes, node.expand(problem))
        nodes = filter_visited(nodes, visited)
        count += 1
        progress(count)
    return None, count


def progress(x):
    print('Nodes Expanded', x, end='\r')


def filter_visited(nodes, visited):
    # print('Nodes')
    # print(nodes)
    # print('Visited')
    # print(visited)
    # print('Removed')
    # print([x for x in nodes if x in visited])
    # nodes = [x for x in nodes if x not in visited]
    nodes = list(set(nodes) - set(visited))
    # print('Filtered')
    # print(nodes)
    return nodes


# ##########################
# Breadth First Search (BFS)
# ##########################


def breadth_first_search(problem):
    return general_search(problem, enqueue_at_end)


def enqueue_at_end(nodes, expanded_nodes):
    nodes.extend(expanded_nodes)
    return nodes


# ########################
# Depth First Search (DFS)
# ########################


def depth_first_search(problem):
    return general_search(problem, enqueue_at_front)


def enqueue_at_front(nodes, expanded_nodes):
    expanded_nodes.extend(nodes)
    return expanded_nodes


# ########################
# Iterative Deepening (ID)
# ########################


def iterative_deepening_search(problem):
    total_count = 0
    for i in itertools.count():
        solution, count = depth_limited_search(problem, i)
        total_count += count
        if solution:
            return solution, total_count


def depth_limited_search(problem, depth):
    cutoff_queue_func = functools.partial(enqueue_at_front_cutoff, depth)
    return general_search(problem, cutoff_queue_func)


def enqueue_at_front_cutoff(depth, nodes, expanded_nodes):
    nodes = enqueue_at_front(nodes, expanded_nodes)
    return [x for x in nodes if x.depth <= depth]


# ########################
# Uniform Cost Search (UC)
# ########################


def uniform_cost_search(problem):
    return general_search(problem, ordered_insert)


def ordered_insert(nodes, expanded_nodes):
    nodes.extend(expanded_nodes)
    ordered_nodes = sorted(nodes, key=operator.attrgetter('path_cost'))
    return ordered_nodes

# ##################
# Greedy Search (GC)
# ##################


def greedy_search_1(problem):
    return best_first_search(problem, heuristic_1)


def heuristic_1(node):
    """returns smallest distance between white walkers or dragon stone and current position"""
    x_node, y_node = node.state.location()
    goals = node.state.grid.components.white_walkers
    goals.append(node.state.grid.components.dragon_stone)
    distance = [np.sqrt((x_node - x)**2 + (y_node - y)**2) for x, y in goals]
    return distance[np.argmin(distance)]


def greedy_search_2(problem):
    return best_first_search(problem, heuristic_2)


def heuristic_2(node):
    """returns sum of distances between white walkers and current position"""
    x_node, y_node = node.state.location()
    goals = node.state.grid.components.white_walkers
    distance = [np.sqrt((x_node - x)**2 + (y_node - y)**2) for x, y in goals]
    return np.sum(distance)


def greedy_search_3(problem):
    return best_first_search(problem, heuristic_3)


def heuristic_3(node):
    """number of white_walkers"""
    return node.state.white_walkers()


def best_first_search(problem, eval_function):
    heuristic_queue_func = functools.partial(ordered_eval_insert, eval_function)
    return general_search(problem, heuristic_queue_func)


def ordered_eval_insert(eval_function, nodes, expanded_nodes):
    nodes.extend(expanded_nodes)
    heuristic_nodes = [(node, eval_function(node)) for node in nodes]
    ordered_nodes = sorted(heuristic_nodes, key=lambda x: x[1])
    return [x for x, y in ordered_nodes]


# ##################
# A Star Search (AC)
# ##################


def a_star_1(problem):
    return best_first_search(problem, a_heuristic_1)


def a_heuristic_1(node):
    return node.path_cost + heuristic_1(node)


def a_star_2(problem):
    return best_first_search(problem, a_heuristic_2)


def a_heuristic_2(node):
    return node.path_cost + heuristic_2(node)


def a_star_3(problem):
    return best_first_search(problem, a_heuristic_3)


def a_heuristic_3(node):
    return node.path_cost + heuristic_3(node)
