"""
A* (A-Star) Pathfinding Algorithm
===================================
Finds the shortest path on a 2D grid using f(n) = g(n) + h(n).

    g(n) — cost from start to current node (actual steps taken)
    h(n) — estimated cost from current node to goal (heuristic)
    f(n) — total estimated cost (used to prioritize exploration)

The heuristic used here is Manhattan Distance:
    h = |current_x - goal_x| + |current_y - goal_y|


"""

import heapq


# ---------------------------------------------------------------------------
# Grid Legend
# ---------------------------------------------------------------------------
# 0 = free cell (walkable)
# 1 = obstacle  (blocked)
# S = start     (printed in visualization)
# G = goal      (printed in visualization)
# * = path      (printed in visualization)

GRID = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0],
]

START = (0, 0)   # (row, col)
GOAL  = (5, 6)   # (row, col)

# The four cardinal directions: up, down, left, right
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


# ---------------------------------------------------------------------------
# Heuristic: Manhattan Distance
# ---------------------------------------------------------------------------
def manhattan(a: tuple, b: tuple) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ---------------------------------------------------------------------------
# Validity Check
# ---------------------------------------------------------------------------
def is_valid(grid: list, row: int, col: int) -> bool:
    """
    Returns True if (row, col) is inside the grid and not an obstacle.
    """
    rows = len(grid)
    cols = len(grid[0])
    return (
        0 <= row < rows and      # within vertical bounds
        0 <= col < cols and      # within horizontal bounds
        grid[row][col] == 0      # cell is not blocked
    )


# ---------------------------------------------------------------------------
# Path Reconstruction
# ---------------------------------------------------------------------------
def reconstruct_path(came_from: dict, current: tuple) -> list:
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()   # reverse so it runs start → goal
    return path


# ---------------------------------------------------------------------------
# A* Algorithm
# ---------------------------------------------------------------------------
def astar(grid: list, start: tuple, goal: tuple):

    # ── Priority queue (min-heap): (f_cost, g_cost, node) ──────────────────
    # heapq always pops the item with the smallest first element (f_cost).
    open_set = []
    heapq.heappush(open_set, (0, 0, start))

    # ── Track where each node was reached from (for path reconstruction) ───
    came_from = {start: None}

    # ── g_cost[node] = cheapest known cost from start to node ──────────────
    g_cost = {start: 0}

    # ── Main search loop ────────────────────────────────────────────────────
    while open_set:

        # Pop the node with the lowest f = g + h
        f, g, current = heapq.heappop(open_set)

        # ── Goal reached — reconstruct and return the path ─────────────────
        if current == goal:
            return reconstruct_path(came_from, current)

        row, col = current

        # ── Explore all 4 neighbours ───────────────────────────────────────
        for dr, dc in DIRECTIONS:
            neighbour = (row + dr, col + dc)

            # Skip if out-of-bounds or blocked
            if not is_valid(grid, neighbour[0], neighbour[1]):
                continue

            # Each step costs 1 (uniform grid)
            tentative_g = g + 1

            # Only proceed if we found a cheaper route to this neighbour
            if tentative_g < g_cost.get(neighbour, float('inf')):

                # Record the cheaper route
                g_cost[neighbour]    = tentative_g
                came_from[neighbour] = current

                # Calculate h and f for the neighbour
                h = manhattan(neighbour, goal)
                f = tentative_g + h   # ← f(n) = g(n) + h(n)

                heapq.heappush(open_set, (f, tentative_g, neighbour))

    # If we exhausted the queue without reaching goal, no path exists
    return None


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------
def visualize(grid: list, path: list, start: tuple, goal: tuple) -> None:
    """
    Prints a text-based grid showing:
      S = start
      G = goal
      * = path (excluding start and goal)
      # = obstacle
      . = free cell
    """
    path_set = set(path)

    print("\n  Grid Visualization:")
    print("  " + "─" * (len(grid[0]) * 2 + 1))

    for r, row in enumerate(grid):
        line = "  │"
        for c, cell in enumerate(row):
            pos = (r, c)
            if pos == start:
                line += "S "
            elif pos == goal:
                line += "G "
            elif pos in path_set:
                line += "* "
            elif cell == 1:
                line += "# "
            else:
                line += ". "
        print(line + "│")

    print("  " + "─" * (len(grid[0]) * 2 + 1))
    print("  S=Start  G=Goal  *=Path  #=Obstacle  .=Free\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 45)
    print("       A* Pathfinding Algorithm Demo")
    print("=" * 45)
    print(f"\n  Start : {START}")
    print(f"  Goal  : {GOAL}")
    print(f"  Grid  : {len(GRID)} rows × {len(GRID[0])} cols\n")

    path = astar(GRID, START, GOAL)

    if path is None:
        print("  ✗ No path found — goal is unreachable.\n")
        # Still visualize the grid so the user can see the obstacles
        visualize(GRID, [], START, GOAL)
        return

    print(f"  ✓ Shortest path found!  Length = {len(path) - 1} steps\n")
    print(f"  Path: {' → '.join(str(p) for p in path)}\n")

    visualize(GRID, path, START, GOAL)

    # ── Show g, h, f for each step ─────────────────────────────────────────
    print("  Step-by-step g / h / f values:")
    print("  " + "-" * 38)
    print(f"  {'Step':<6}{'Node':<12}{'g':>4}{'h':>6}{'f':>6}")
    print("  " + "-" * 38)
    for step, node in enumerate(path):
        g = step                         # uniform cost: 1 per step
        h = manhattan(node, GOAL)        # Manhattan distance to goal
        f = g + h
        marker = " ← start" if node == START else (" ← goal" if node == GOAL else "")
        print(f"  {step:<6}{str(node):<12}{g:>4}{h:>6}{f:>6}{marker}")
    print()


if __name__ == "__main__":
    main()

# In short: Dijkstra = A* with h(n) = 0 for every node.
#           A* adds "direction" to Dijkstra's exhaustive search.
# =============================================================================
