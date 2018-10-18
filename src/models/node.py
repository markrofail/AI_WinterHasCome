class Node:
    """Abstract Class: Formal Node"""
    # A Node is defined as a 5-tuple:

    # 1. The state of the state space that this node corresponds to.
    state = None

    # 2. The parent node.
    parent = None

    # 3. The operator applied to generate this node.
    operator = None

    # 4. The depth of the node in the tree.
    depth = None

    # 5. The path cost from the root.
    path_cost = None

    # *. Node Constructor
    def __init__(self, state, parent=None, operator=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.operator = operator
        self.path_cost = path_cost

        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def expand(self, problem):
        """applies all **valid** operators on current state"""
        return [self.child_node(problem, operator)
                for operator in problem.valid_operators(self.state)]

    def child_node(self, problem, operator):
        """creates a child node by applying an operator on current state"""
        child_state = problem.result(self.state, operator)
        path_cost = self.path_cost+problem.cost_function(operator)

        return Node(
            state=child_state,
            parent=self,
            operator=operator,
            path_cost=path_cost
        )

    def path(self):
        """list of nodes from the root to this node."""
        node = self
        node_path = list()
        while True:
            node_path.append(node)
            node = node.parent
            if not node:
                return list(reversed(node_path))

    def __repr__(self):
        return self.state.__repr__()

    def __lt__(self, node):
        return self.state < node.state

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return self.state.__hash__()