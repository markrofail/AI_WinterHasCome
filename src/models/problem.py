from src.models.operator import Operators
from src.models.state import SwState


class Problem:
    """Abstract Class: Formal Problem"""
    # A problem is defined as a 5-tuple:

    # 1. A set of operators, or actions, available to the agent.
    def valid_operators(self, state):
        pass

    # 2. An initial state.
    initial_state = None

    # 3. A state space: the set of states reachable from the initial state by
    # any sequence of actions.
    def result(self, state, operator):
        """resultant state from performing the given operator on the given state."""
        pass

    # 4. A goal test, which the agent applies to a state to determine if it is
    # a goal state.
    def goal_test(self, state):
        """goal predicate"""
        pass

    # 5. A path cost function: a function that assigns cost to a sequence of
    # actions
    def cost_function(self, actions):
        """sum of action sequence"""
        pass


class SwProblem(Problem):

    # 2. An initial state.
    initial_state = None

    # *. Problem Constructor
    def __init__(self, grid):
        self.initial_state = SwState(
            grid=grid,
        )

    # 3. A state space: the set of states reachable from the initial state by
    # any sequence of actions.
    def result(self, state, operator):
        """resultant state from performing the given operator on the given state."""
        moving_operators = [Operators.LEFT, Operators.RIGHT, Operators.FORWARD, Operators.BACKWARD]
        if operator in moving_operators:
            x, y = state.location()

            if operator == Operators.LEFT:
                x -= 1
            if operator == Operators.RIGHT:
                x += 1
            if operator == Operators.FORWARD:
                y -= 1
            if operator == Operators.BACKWARD:
                y += 1

            new_location = x, y
            return SwState(
                grid=state.grid,
                location=new_location,
            )

        else:
            return SwState(
                grid=state.grid,
                white_walkers=True,
            )

    # 4. A goal test, which the agent applies to a state to determine if it is
    # a goal state.
    def goal_test(self, state):
        """goal predicate"""
        return state.white_walkers() == 0

    # 5. A path cost function: a function that assigns cost to a sequence of
    # actions
    def cost_function(self, action):
        """sum of action sequence"""
        cost_dict = dict([
            (Operators.LEFT, 2),
            (Operators.RIGHT, 2),
            (Operators.FORWARD, 2),
            (Operators.BACKWARD, 2),
            (Operators.KILL, 3),
        ])
        return cost_dict[action]

    # 1. A set of operators, or actions, available to the agent.
    def valid_operators(self, state):
        """list of **valid** action to be performed on state"""
        operators = list()
        x, y = state.location()

        if state.grid.is_safe_location((x - 1, y)):
            operators.append(Operators.LEFT)

        if state.grid.is_safe_location((x + 1, y)):
            operators.append(Operators.RIGHT)

        if state.grid.is_safe_location((x, y - 1)):
            operators.append(Operators.FORWARD)

        if state.grid.is_safe_location((x, y + 1)):
            operators.append(Operators.BACKWARD)

        has_dragon_glass = state.dragon_glass() > 0
        ww_locations = state.grid.nearby_white_walkers(state.location())
        ww_surrounding = len(ww_locations) > 0

        if has_dragon_glass and ww_surrounding:
            operators.append(Operators.KILL)
        return operators
