# Week 4 — Local Search and Optimisation

**TU850-3**  
**AINL3001 — Knowledge-Driven AI**  
**Dr. Bianca Schoen-Phelan**  
**2026**

## Learning Objectives

By the end of this lab you should be able to:

- Explain the difference between search and optimisation.
- Represent a candidate solution as a state.
- Use the common `Problem` representation introduced this week.
- Distinguish between an **action** and the **state resulting from an action**.
- Evaluate candidate solutions using a cost function.
- Implement Hill Climbing.
- Explain local minima and plateaus.
- Implement Simulated Annealing.
- Compare deterministic and stochastic search methods.
- Relate optimisation techniques to Machine Learning.

## A Common Problem Representation

During Weeks 1–3, we represented AI problems directly using
variables, functions and data structures.

For example, in Week 1 we used:

    START_STATE = (0, 0)
    GOAL_STATE = (4, 4)

    def get_neighbours(state):
        ...

As our problems and algorithms become more complex, we now want
a consistent way of representing problems.

From this week onwards, we will use the `Problem` class provided
in:

    common/problem.py

Earlier labs                  Common representation

START_STATE                   problem.initial
GOAL_STATE                    problem.goal
possible moves                problem.actions(state)
state transition              problem.result(state, action)
state == GOAL_STATE           problem.goal_test(state)

## Structure for this Lab

common/problem.py
        ↓
defines what a Problem looks like

week04/grid_problem.py
        ↓
defines this particular problem

week04/hill_climbing_starter.py
        ↓
implements an algorithm that tries to solve it



# 1. From Search to Optimisation

In previous weeks, we focused on finding paths through a state space using algorithms such as:

- Breadth-First Search (BFS),
- Depth-First Search (DFS),
- Greedy Search,
- A*.

In these problems, the path taken through the state space matters.

This week we investigate **local search and optimisation**.

For many optimisation problems, we are less interested in the path taken and more interested in finding a good final state.

Examples include:

- Timetabling,
- Scheduling,
- Resource allocation,
- Route optimisation,
- Hyperparameter tuning in Machine Learning.

A key new idea is that we need a way to measure **how good a candidate solution is**.


# 2. A Common Problem Representation

So far, our labs have represented problems directly using variables and functions.

From this week onwards, where appropriate, we will use a common `Problem` class.

It is located in:

```text
common/problem.py
```

The basic structure is:

```python
class Problem:

    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        return state == self.goal
```

This gives us a common vocabulary for describing different problems:

- `initial` — where we start
- `goal` — the goal, if there is a known goal state
- `actions(state)` — what can we do from this state?
- `result(state, action)` — what state results from performing an action?
- `goal_test(state)` — have we reached the goal?

The important idea is that `Problem` does **not** know anything about grids, queens, search algorithms, or optimisation.

Specific problems provide those details.


# 3. Tutorial — Revisiting the Grid World

Before starting local search, complete the short tutorial:

```text
problem_tutorial_starter.py
```

This uses the grid world from previous weeks to introduce the `Problem` structure.

Complete:

```python
class GridProblem(Problem):
```

by implementing:

```python
actions(state)
```

and:

```python
result(state, action)
```

For example, from:

```python
(0, 0)
```

the available actions should be:

```text
DOWN
RIGHT
```

Applying the action:

```text
RIGHT
```

should produce:

```python
(1, 0)
```

### Tutorial Reflection

Be ready to discuss:

1. What information is stored in `problem.initial`?
2. What information is stored in `problem.goal`?
3. What is the difference between `actions(state)` and `result(state, action)`?
4. Why doesn't `Problem` know anything about grids?
5. Why doesn't `GridProblem` know anything about search?
6. Could the same `Problem` structure represent something other than a grid?

Once you are comfortable with this representation, move on to the main lab.


# 4. The N-Queens Problem

We will explore local search using the **N-Queens problem**.

The challenge is to place N queens on a chessboard so that no queen attacks another queen.

Queens can attack:

- Horizontally,
- Vertically,
- Diagonally.

For the main lab we will use:

```python
N = 8
```

Our objective is therefore to find a board containing eight queens with **zero conflicts**.


# 5. State Representation

A state represents a complete candidate solution.

For example:

```python
[0, 4, 7, 5, 2, 6, 1, 3]
```

Each index represents a **column**.

Each value represents the **row containing the queen**.

Therefore:

```text
Column 0 -> Row 0
Column 1 -> Row 4
Column 2 -> Row 7
Column 3 -> Row 5
Column 4 -> Row 2
Column 5 -> Row 6
Column 6 -> Row 1
Column 7 -> Row 3
```

Notice that this representation automatically places exactly one queen in every column.


# 6. The Queens Problem

The file:

```text
queens_problem.py
```

contains the representation of the N-Queens problem.

It defines:

```python
class QueensProblem(Problem):
```

Just like `GridProblem`, it provides:

```python
problem.actions(state)
problem.result(state, action)
```

However, an action is now different.

In the grid world, an action looked like:

```python
"RIGHT"
```

For N-Queens, an action is represented as:

```python
(column, new_row)
```

For example:

```python
(3, 5)
```

means:

> Move the queen in column 3 to row 5.

This demonstrates why `Problem` is useful: different problems can have completely different states and actions while still sharing the same general structure.


# 7. Task 0 — Manual Exploration

Consider the following board:

```python
[0, 1, 2, 3]
```

Before writing any code, consider the following questions:

1. How many pairs of queens are attacking each other?
2. Does this represent a valid solution?
3. If one queen moved, could the number of conflicts decrease?

### Discussion

Why might an AI system need a way to measure the quality of a candidate solution?


# 8. Task 1 — Cost Function

Implement:

```python
count_conflicts(board)
```

The function should calculate the number of **pairs of queens that attack each other**.

The number of conflicts is our **cost function**.

For this problem:

```text
lower cost = better solution
```

A perfect solution has:

```text
cost = 0
```

Think carefully about when two queens attack each other.

# 9. Task 2 — Generate Neighbours

A **neighbour** is another candidate solution that can be reached by making a small change to the current state.

For N-Queens, a neighbour is produced by:

- Moving one queen to another row.
- Keeping all other queens fixed.

Use the problem interface:

```python
problem.actions(state)
```

to obtain the possible actions and:

```python
problem.result(state, action)
```

to produce the corresponding states.

Implement:

```python
generate_neighbours(problem, board)
```

### Questions

For an 8×8 board:

1. How many alternative rows can each queen move to?
2. How many neighbours should therefore be generated?
3. Why might generating every neighbour become expensive for large boards?

Use your answer to Question 2 as a useful check on your implementation.


# 10. Task 3 — Hill Climbing

Now implement:

```python
hill_climbing(problem, start_board)
```

Hill Climbing repeatedly moves to a better neighbouring state.

The basic algorithm is:

```text
1. Start with a candidate solution.

2. Evaluate the current state.

3. Generate neighbouring states.

4. Find the neighbour with the lowest cost.

5. If that neighbour is better:
       move to it.

6. Otherwise:
       stop.

7. Repeat.
```

Remember:

```text
lower conflict count = better state
```

A board with:

```text
0 conflicts
```

is a solution.


# 11. Task 4 — Experiment with Hill Climbing

Run Hill Climbing several times using different random starting boards.

Record the final cost.

| Attempt | Final Cost |
|---|---:|
| 1 | 0 |
| 2 | 1 |
| 3 | 1 |
| 4 | 2 |
| 5 | 1 |

Consider:

- Does Hill Climbing always find a solution?
- Does it sometimes stop with conflicts remaining?
- Why does it stop if a better neighbour cannot be found?


# 12. Local Minima and Plateaus

Hill Climbing only considers whether a neighbouring state is better than the current state.

This creates an important problem.

The algorithm may reach a state where:

```text
no neighbour has a lower cost
```

even though:

```text
cost > 0
```

This is a **local minimum**.

The algorithm may also encounter a **plateau**, where many neighbouring states have the same cost.

Hill Climbing cannot easily escape these situations because it does not normally accept worse states.

This motivates our next algorithm.


# 13. Task 5 — Simulated Annealing

Implement:

```python
simulated_annealing(problem, start_board)
```

Simulated Annealing differs from Hill Climbing because it can sometimes accept a **worse state**.

At first, the probability of accepting worse moves is relatively high.

As the temperature decreases, worse moves become less likely to be accepted.

This allows the algorithm to:

- Explore more widely early in the search.
- Potentially escape local minima.
- Become increasingly selective later in the search.

### Questions

1. Why might accepting a worse move sometimes be useful?
2. How does the algorithm behave when the temperature is high?
3. How does its behaviour change as the temperature decreases?


# 14. Task 5.1 — Compare the Algorithms

Run both algorithms multiple times.

Record the best cost you find.

| Algorithm | Best Cost Found |
|---|---:|
| Hill Climbing | 0 (only 1 of 5 runs; usually stuck at 1–2) |
| Simulated Annealing | 0 (most runs with `cooling_rate = 0.999`) |

Consider the behaviour you observed:

- Do both algorithms always produce the same result?
- Which algorithm shows more variation between runs?
- How does accepting occasional worse moves affect the search?
- What trade-off does Simulated Annealing introduce?


# 15. Deterministic and Stochastic Search

Hill Climbing selects an improving neighbouring state according to its evaluation function.

Simulated Annealing introduces randomness into the decision process.

This gives us an important distinction:

**Deterministic behaviour**

Given the same state and the same decision rule, the algorithm makes the same choice.

**Stochastic behaviour**

Randomness influences some of the algorithm's decisions.

Many optimisation and Machine Learning techniques use stochastic behaviour because exploring different parts of a search space can help avoid poor local solutions.


# 16. GitHub Task

Commit your work regularly rather than waiting until the entire lab is complete.

For example:

```text
Implemented conflict function
```

```text
Implemented neighbour generation
```

```text
Implemented Hill Climbing
```

```text
Implemented Simulated Annealing
```

Use:

```bash
git status
```

to check which files have changed before committing.

Your Git history should show the development of your solution over time.


# 17. Reflection Questions

Complete these after finishing the main tasks.

1. What is the difference between search and optimisation?
2. Why does an optimisation problem require a way to evaluate candidate solutions?
3. Why can Hill Climbing become stuck in a local minimum?
4. What is a plateau?
5. How does Simulated Annealing attempt to overcome the limitations of Hill Climbing?
6. What is the difference between deterministic and stochastic search?
7. How did the `Problem` representation allow us to represent both a grid world and N-Queens?
8. How do optimisation techniques such as these relate to Machine Learning?

### Answers

**1. What is the difference between search and optimisation?**
Search looks for a path from an initial state to a goal state, and the path itself matters (e.g. the route through the grid world). Optimisation looks for the best possible final state according to a cost function; the path taken to reach it does not matter. In N-Queens we only care about the final board, not the moves that produced it.

**2. Why does an optimisation problem require a way to evaluate candidate solutions?**
There is often no single known goal state to compare against (`goal=None` in `QueensProblem`). The cost function (`count_conflicts`) tells the algorithm how good a board is, so it can compare neighbours and decide which direction is an improvement. Without it the algorithm has no way to tell better states from worse ones.

**3. Why can Hill Climbing become stuck in a local minimum?**
Hill Climbing only moves to a neighbour that is strictly better than the current state. If every neighbour has the same or higher cost, it stops, even if the cost is still above 0. In our runs it often stopped with 1 or 2 conflicts remaining because no single queen move could reduce the count, even though a solution existed elsewhere in the search space.

**4. What is a plateau?**
A plateau is a region of the search space where many neighbouring states have the same cost. Because no neighbour is better, Hill Climbing has no direction to move in and stops (our implementation stops when the best neighbour is not strictly better).

**5. How does Simulated Annealing attempt to overcome the limitations of Hill Climbing?**
It picks a random neighbour and always accepts it if it is better, but also accepts a worse neighbour with probability `e^(-delta / T)`. When the temperature is high, worse moves are accepted often, so the algorithm explores widely and can climb out of local minima. As the temperature cools, worse moves become rare and it behaves more like Hill Climbing. With slow cooling (0.999) it solved 29 of 30 boards, compared with 4 of 30 for Hill Climbing. With fast cooling (0.95) it had too few steps and solved none, which shows the trade-off between solution quality and runtime.

**6. What is the difference between deterministic and stochastic search?**
A deterministic algorithm always makes the same choice from the same state; Hill Climbing always picks the lowest-cost neighbour, so the same start board always gives the same result. A stochastic algorithm uses randomness in its decisions; Simulated Annealing picks random neighbours and accepts worse moves by chance, so the same start board can give different results on different runs.

**7. How did the `Problem` representation allow us to represent both a grid world and N-Queens?**
`Problem` only defines a general interface: `initial`, `goal`, `actions(state)`, `result(state, action)` and `goal_test(state)`. It knows nothing about grids or queens. `GridProblem` fills these in with `(x, y)` states and `"UP"/"DOWN"/"LEFT"/"RIGHT"` actions, while `QueensProblem` uses a list of rows as the state and `(column, new_row)` as the action. Because both follow the same interface, algorithms such as `generate_neighbours` work without knowing which problem they are solving.

**8. How do optimisation techniques such as these relate to Machine Learning?**
Training a Machine Learning model is an optimisation problem: the state is the model's parameters and the cost function is the loss. Gradient descent is similar to Hill Climbing: it repeatedly moves the parameters in the direction that lowers the loss, and it can also get stuck in local minima. Stochastic techniques such as stochastic gradient descent, random initialisation and hyperparameter search use randomness in the same way Simulated Annealing does, to explore the search space and avoid poor local solutions.


# Extensions

Complete these only after finishing the main lab.

## Extension 1 — Visualise the Board

Create a function that displays the board using:

```text
Q = Queen
. = Empty square
```

For example:

```text
Q . . .
. . Q .
. . . .
. Q . .
```

Use your visualisation to compare the starting and final boards.


## Extension 2 — Random Restart Hill Climbing

One way to address local minima is simply to try again from a different starting state.

Implement **Random Restart Hill Climbing**.

The idea is:

```text
generate random state
        ↓
run Hill Climbing
        ↓
solution found?
   ↓           ↓
  yes          no
   ↓           ↓
 stop      restart
```

Experiment with different numbers of restarts.

Consider:

1. Does performance improve?
2. Why might random restarts help?
3. What additional computational cost do they introduce?


## Extension 3 — Larger Boards

Try larger values of N.

For example:

```python
N = 20
```

and:

```python
N = 50
```

Observe:

- Runtime
- Number of possible neighbours
- Final solution quality
- Hill Climbing behaviour
- Simulated Annealing behaviour

Consider how increasing the size of the problem affects the size of the search space.


# Week 4 Summary

This week marks a change in how we think about AI search.

In earlier weeks, we asked:

> **How can we find a path from the initial state to a goal?**

In local search and optimisation, we instead ask:

> **How can we improve a candidate solution?**

The central ideas are:

```text
State
  ↓
Generate Neighbours
  ↓
Evaluate Candidates
  ↓
Choose a Move
  ↓
Repeat
```

Hill Climbing always tries to improve the current state but can become trapped in local minima or plateaus.

Simulated Annealing introduces stochastic behaviour, allowing occasional worse moves in an attempt to explore the search space more effectively.

These ideas provide an important foundation for later optimisation techniques and for understanding optimisation in Machine Learning.