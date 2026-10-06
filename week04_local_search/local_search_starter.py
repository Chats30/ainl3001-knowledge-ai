"""
AINL3001 — Knowledge-Driven AI
Week 4 — Local Search and Optimisation
BSP 2026

This week introduces local search.

In previous weeks, search algorithms explored paths through
a state space in order to reach a goal.

Local search takes a different approach:

    1. Start with a state.
    2. Evaluate how good that state is.
    3. Generate neighbouring states.
    4. Move to a better neighbour.
    5. Repeat.

We will explore this using the N-Queens problem.

Tasks
-----

1. Understand the problem representation.
2. Implement conflict counting.
3. Explore neighbouring states.
4. Implement Hill Climbing.
5. Implement Simulated Annealing.
"""

import math
import random

from queens_problem import QueensProblem

N = 8


# --------------------------------------------------
# TASK 0 — UNDERSTANDING THE STATE
# --------------------------------------------------

example_board = [0, 1, 2, 3]

print("Manual Exploration Board:")
print(example_board)

print(
    "\nEach list position represents a column."
)

print(
    "Each value represents the row containing the queen."
)

print(
    "\nQuestion: How many conflicts exist on this board?"
)


# --------------------------------------------------
# TASK 1 — EVALUATE A STATE
# --------------------------------------------------

def count_conflicts(board):
    """
    Return the number of pairs of queens
    that attack each other.

    Lower values are better.

    A solution has:

        conflict count = 0
    """

    conflicts = 0

    # compare each queen with every queen to its right (so ecah pair is counted once)
    for i in range(len(board)):
        for j in range(i + 1, len(board)):

            # Same row: both queens have the smae row value
            same_row = board[i] == board[j]

            # same diagonal: row distance equals column distance
            same_diagonal = abs(board[i] - board[j]) == abs(i - j)
            
            if same_row or same_diagonal:
                conflicts += 1
    return conflicts

# --------------------------------------------------
# TASK 2 — EXPLORE THE PROBLEM
# --------------------------------------------------

def generate_neighbours(problem, board):
    """
    Generate all neighbouring boards.

    Use the Problem interface introduced this week:

        problem.actions(state)
        problem.result(state, action)
    """

    neighbours = []

    # Ask the problem which moves are possible from this board
    for action in problem.actions(board):
        # Apply the move to get a new board (Oroginal un=changed)
        new_board = problem.result(board, action)

        # Store the new board as a neighbour
        neighbours.append(new_board)

    return neighbours


# --------------------------------------------------
# TASK 3 — HILL CLIMBING
# --------------------------------------------------

def hill_climbing(problem, start_board):
    """
    Use Hill Climbing to reduce the number
    of conflicts.

    Algorithm:

        current = start state

        repeat:

            generate neighbours

            find the neighbour with the
            lowest conflict count

            if the neighbour is not better:
                stop

            otherwise:
                move to the neighbour

        return current
    """

    current = start_board

    while True:

        # Stop early if the board is already solved 
        if count_conflicts(current) == 0:
            return current
        
        # Generate every board one  ove away
        neighbours = generate_neighbours(problem, current)

        # Pick the neighbour with the fewest conflicts
        best = min(neighbours, key=count_conflicts)

        # If it isnt strictly better were stuck (local min or plateau)
        if count_conflicts(best) >= count_conflicts(current):
            return current
        
        # Otherwise move to the better board and repeat
        current = best

    


# --------------------------------------------------
# TASK 4 — SIMULATED ANNEALING
# --------------------------------------------------

def simulated_annealing(problem, start_board):
    """
    Use Simulated Annealing to search for
    a solution.

    Unlike Hill Climbing, Simulated Annealing
    can sometimes accept a worse state.

    This can help escape local minima.
    """

    current = start_board

    temperature = 10.0
    cooling_rate = 0.999

    

    # Keeps going until the system has cooled almost completely
    while temperature > 0.1:

        # Stop if the board is solved 
        if count_conflicts(current) == 0:
            return current
        
        # Pick one random neighbour
        neighbour = random.choice(generate_neighbours(problem, current))

        # How much worse is the neighbour? (negative = better)
        delta = count_conflicts(neighbour) - count_conflicts(current)

        # Always accept a better move 
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current = neighbour
        
        # Cool down: worse moves become lesss likely over time 
        temperature *= cooling_rate

    return current




# --------------------------------------------------
# TESTING AREA
# --------------------------------------------------

if __name__ == "__main__":

    board = [
        random.randint(0, N - 1)
        for _ in range(N)
    ]

    problem = QueensProblem(board)

    print("\nRandom Board")
    print(board)

    print("\nConflicts")
    print(
        count_conflicts(board)
    )

    print("\nPossible Actions")

    actions = problem.actions(board)

    print(
        f"{len(actions)} actions available"
    )

    print("\nNeighbours")

    neighbours = generate_neighbours(
        problem,
        board
    )

    print(
        f"{len(neighbours)} neighbours generated"
    )

    print("\nHill Climbing")

    final = hill_climbing(problem, board)

    print("Start:", board, "cost", count_conflicts(board))
    print("Final:", final, "cost", count_conflicts(final))

    print("\nSimulated Annealing")

    final_sa = simulated_annealing(problem, board)

    print("Final:", final_sa, "cost", count_conflicts(final_sa))

