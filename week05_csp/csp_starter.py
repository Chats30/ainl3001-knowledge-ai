"""
AINL3001 — Knowledge-Driven AI
Week 5 — Constraint Satisfaction Problems
BSP 2026

Australian map colouring: six regions and three colours.

Tasks
-----
0. Examine an invalid assignment.
1. Understand variables, domains and constraints.
2. Implement constraint checking.
3. Implement backtracking with simple variable selection.
4. Compare backtracking with brute force.
5. Improve variable selection using MRV.

Work in this starter file and commit your progress to your own fork.
"""

# --------------------------------------------------
# TASK 0 — MANUAL EXPLORATION
# --------------------------------------------------

example_assignment = {
    "WA": "Red",
    "NT": "Red",
    "SA": "Green",
    "Q": "Blue",
    "NSW": "Red",
    "V": "Green",
}

print("Manual CSP Exploration")
print(example_assignment)
print("\nQuestions:")
print("1. Is this assignment valid?")
print("2. Which neighbouring pairs violate a constraint?")
print("3. How could you correct the assignment?")
print("4. Why is it useful to detect violations early?")

# Task 0: Spots the two clashes (WA-NT and SA-V) in an invalid colouring by hand.

# --------------------------------------------------
# TASK 1 — CSP REPRESENTATION
# --------------------------------------------------

# Task 1: Models the problem as variables (regions), domains (colours) and constraints (neighbours differ).
variables = ["WA", "NT", "SA", "Q", "NSW", "V"]

# Each region may use one of these three colours.
domains = {
    variable: ["Red", "Green", "Blue"]
    for variable in variables
}

# Each pair of neighbouring regions must have different colours.
constraints = [
    ("WA", "NT"),
    ("WA", "SA"),
    ("NT", "SA"),
    ("NT", "Q"),
    ("SA", "Q"),
    ("SA", "NSW"),
    ("SA", "V"),
    ("Q", "NSW"),
    ("NSW", "V"),
]

# --------------------------------------------------
# TASK 2 — CONSTRAINT CHECKING
# --------------------------------------------------

def is_valid_assignment(assignment):
    """Return True if a complete OR partial assignment is valid."""
    # Task 2: Returns False if any two assigned neighbours share a colour, else True.
    for a, b in constraints:
        if a in assignment and b in assignment:
            if assignment[a] == assignment[b]:
                return False
    return True


# --------------------------------------------------
# TASK 3 AND TASK 5 — VARIABLE SELECTION
# --------------------------------------------------

def select_unassigned_variable(assignment):
    """Choose the next unassigned region.

    Task 3: First return the FIRST unassigned region.

    Task 5: Replace that approach with MRV (Minimum Remaining Values):
    choose the unassigned region with the FEWEST currently legal
    colours. Break ties by keeping the first region in variables.
    """
    # Tasks 3 & 5: Picks the unassigned region with the fewest legal colours (MRV), first on ties.
    best_var = None
    best_count = None
    for var in variables:
        if var in assignment:
            continue
        legal = 0
        for colour in domains[var]:
            assignment[var] = colour
            if is_valid_assignment(assignment):
                legal += 1
            del assignment[var]
        if best_count is None or legal < best_count:
            best_var, best_count = var, legal
    return best_var


# --------------------------------------------------
# TASK 3 — BACKTRACKING SEARCH
# --------------------------------------------------

def backtracking_search(assignment):
    """Return a complete valid assignment, or None if none exists."""
    # Task 3: Recursively tries colours, abandoning any choice that breaks a constraint.
    global nodes_explored
    if len(assignment) == len(variables):
        return assignment.copy()

    var = select_unassigned_variable(assignment)
    for colour in domains[var]:
        assignment[var] = colour
        nodes_explored += 1
        if is_valid_assignment(assignment):
            result = backtracking_search(assignment)
            if result is not None:
                return result
        del assignment[var]
    return None


# --------------------------------------------------
# TASK 4 — BRUTE FORCE COMPARISON
# --------------------------------------------------

# Task 4: Counts brute-force tests (up to 729) versus backtracking's far fewer, since it prunes early.

nodes_explored = 0


def brute_force_count():
    """Count complete assignments brute force would test until a solution."""
    from itertools import product
    tested = 0
    for colours in product(["Red", "Green", "Blue"], repeat=len(variables)):
        tested += 1
        if is_valid_assignment(dict(zip(variables, colours))):
            break
    return tested


# --------------------------------------------------
# TESTING AREA
# --------------------------------------------------

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("WEEK 5 — CONSTRAINT SATISFACTION PROBLEMS")
    print("=" * 50)

    print("\nVariables:", variables)
    print("Domains:", domains)
    print("Constraints:", constraints)

    print("\nExample assignment valid?")
    print(is_valid_assignment(example_assignment))  # Expected: False

    partial_assignment = {"WA": "Red", "NT": "Green"}
    print("\nPartial assignment valid?")
    print(is_valid_assignment(partial_assignment))  # Expected: True

    print("\nSearching for a solution...")
    solution = backtracking_search({})
    print("Solution:", solution)

    if solution is not None:
        print("\nSolution valid?", is_valid_assignment(solution))
        print("\nColour assignment:")
        for region in variables:
            print(f"{region:4} -> {solution[region]}")
    else:
        print("No solution yet. Complete the TODO sections.")

    print("\nPossible complete assignments:", 3 ** len(variables))
    print("Brute force tested (until first solution):", brute_force_count())
    print("Backtracking (MRV) assignments tried:", nodes_explored)
    print("\nReflection:")
    print("1. What causes backtracking?")
    print("2. Why can backtracking be faster than brute force?")
    print("3. Why might MRV reduce search?")
    print("4. How could this model represent timetabling?")