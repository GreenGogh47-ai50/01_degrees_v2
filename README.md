## Usage
1. Set up the virtual environment and install requirements

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Running, Linting, and Testing the program

Run: `make run`
Lint: `make lint`
Test: `make test`
Submit: `make submit`

## Notes and Explanations
Search problems must contain:
  - An initial state (starting point)
  - actions (the connections we can check)
  - transition models (the result of an action)
  - a goal test (if we reached a conneciton)
  - a path cost function (the steps of seperation to mr bacon)

Other helpful info
  - we need a frontier (empty set of explored nodes) so we don't backtrack
  - actors are nodes
  - the initial state is the first 'parent node'

In class we covered these algorithms:
  - DFS: a 'deep' (stack) search. This would eventually find a solution, but it might not be the shortest path.
  - BFS: a 'wide' (queue) search. Because it expands outwards in all direcitons, it will find the shortest path.
  - Greedy best-first search: I don't see a way to 'map' the actors on a grid, so I don't see a way to create a "heuristic function" (or estimate) of how far away the goal is.
  - A* Search: A modification of greedy best-first, so I can't use this.
  - Minimax: This is for games with an opponent (like tic-tac-toe), so this will be useful in the next project!