import click
from src.models.strategy import Strategies
from src import search as sc
from src.models.problem import SwProblem
from src import generate


def search(grid, strategy, visualize):
    problem = SwProblem(grid)
    print('Initial State:\n', grid)

    if strategy == Strategies.BF:
        solution, count = sc.breadth_first_search(problem)
    if strategy == Strategies.DF:
        solution, count = sc.depth_first_search(problem)
    if strategy == Strategies.ID:
        solution, count = sc.iterative_deepening_search(problem)
    if strategy == Strategies.UC:
        solution, count = sc.uniform_cost_search(problem)
    if strategy == Strategies.GR_1:
        solution, count = sc.greedy_search_1(problem)
    if strategy == Strategies.GR_2:
        solution, count = sc.greedy_search_2(problem)
    if strategy == Strategies.GR_3:
        solution, count = sc.greedy_search_3(problem)
    if strategy == Strategies.AS_1:
        solution, count = sc.a_star_1(problem)
    if strategy == Strategies.AS_2:
        solution, count = sc.a_star_2(problem)
    if strategy == Strategies.AS_3:
        solution, count = sc.a_star_3(problem)

    print('Total number of expanded nodes:', count)
    if solution:
        print('Total solution path cost:', solution.path_cost)
        if visualize:
            print('Solution Trace:')
            visualize_solution(solution)
    else:
        print('No solution')


def visualize_solution(node):
    trace = node.path()
    for x in trace:
        print(x)


@click.command()
@click.option(
    '--strategy',
    type=int,
    default=0,
    help='search strategy to use'
)
@click.option(
    '--visualize',
    is_flag=True,
    help='print trace'
)
def main(strategy=0, visualize=False):
    grid_instance = generate.gen_grid()
    search(grid_instance, strategy, visualize=visualize)


if __name__ == '__main__':
    main()
