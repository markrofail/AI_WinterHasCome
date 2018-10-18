#################################################################################
# GLOBALS                                                                       #
#################################################################################
MAKEFLAGS = -s

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PYTHON_INTERPRETER = python

VISUALIZE=

#################################################################################
# COMMANDS                                                                		#
#################################################################################
.PHONY: generate
## Generates Grid
generate:
	$(PYTHON_INTERPRETER) -m src.generate

.PHONY: visualize
visualize:
	$(eval VISUALIZE=--visualize)

.PHONY: breadth_first
breadth_first:
	$(PYTHON_INTERPRETER) -m src.main --strategy=0 $(VISUALIZE)

.PHONY: depth_first
depth_first:
	$(PYTHON_INTERPRETER) -m src.main --strategy=1 $(VISUALIZE)

.PHONY: iterative_deepening
iterative_deepening:
	$(PYTHON_INTERPRETER) -m src.main --strategy=2 $(VISUALIZE)

.PHONY: uniform_cost
uniform_cost:
	$(PYTHON_INTERPRETER) -m src.main --strategy=3 $(VISUALIZE)

.PHONY: greedy_1st
greedy_1st:
	$(PYTHON_INTERPRETER) -m src.main --strategy=4 $(VISUALIZE)

.PHONY: greedy_2nd
greedy_2nd:
	$(PYTHON_INTERPRETER) -m src.main --strategy=5 $(VISUALIZE)

.PHONY: greedy_3rd
greedy_3rd:
	$(PYTHON_INTERPRETER) -m src.main --strategy=6 $(VISUALIZE)

.PHONY: astar_1st
astar_1st:
	$(PYTHON_INTERPRETER) -m src.main --strategy=7 $(VISUALIZE)

.PHONY: astar_2nd
astar_2nd:
	$(PYTHON_INTERPRETER) -m src.main --strategy=8 $(VISUALIZE)

.PHONY: astar_3rd
astar_3rd:
	$(PYTHON_INTERPRETER) -m src.main --strategy=9 $(VISUALIZE)
