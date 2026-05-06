"""
bellman_ford.py
===============
A clean, educational implementation of the Bellman-Ford algorithm.

The Bellman-Ford algorithm computes shortest paths from a single source
vertex to all other vertices in a weighted directed graph. Unlike Dijkstra's
algorithm, it correctly handles graphs with negative edge weights and can
detect negative-weight cycles.

Time Complexity : O(V * E)  — V vertices, E edges
Space Complexity: O(V)      — distance and predecessor arrays

"""

from __future__ import annotations

# A graph edge is represented as a tuple: (source_vertex, dest_vertex, weight)
Edge = tuple[int, int, int | float]


# ---------------------------------------------------------------------------
# Core algorithm
# ---------------------------------------------------------------------------

def bellman_ford(
    graph: list[Edge],
    num_vertices: int,
    source: int,
) -> tuple[list[float], list[int | None]] | None:
    """Run the Bellman-Ford algorithm on a weighted directed graph.

    Parameters
    ----------
    graph:
        Edge list where each element is ``(u, v, weight)``, representing a
        directed edge from vertex ``u`` to vertex ``v`` with the given weight.
    num_vertices:
        Total number of vertices in the graph (vertices are assumed to be
        labelled ``0 … num_vertices - 1``).
    source:
        The starting vertex from which all shortest paths are computed.

    Returns
    -------
    ``(distances, predecessors)`` on success, or ``None`` if a negative-weight
    cycle is reachable from the source vertex.

    - ``distances[v]`` holds the shortest known distance from *source* to *v*.
    - ``predecessors[v]`` holds the vertex that comes just before *v* on the
      shortest path from *source*, enabling full path reconstruction.
    """

    # ------------------------------------------------------------------
    # Step 1 – Initialise distances and predecessors
    # ------------------------------------------------------------------
    # Every vertex starts as "infinitely far away" and without a predecessor.
    # The source vertex is distance 0 from itself.
    INFINITY = float("inf")
    distances: list[float] = [INFINITY] * num_vertices
    predecessors: list[int | None] = [None] * num_vertices

    distances[source] = 0

    # ------------------------------------------------------------------
    # Step 2 – Relax all edges exactly (V - 1) times
    # ------------------------------------------------------------------
    # Why V - 1?  The longest possible shortest path in a graph without
    # negative cycles visits at most V - 1 edges.  Each full pass over every
    # edge is guaranteed to "settle" at least one more vertex, so V - 1 passes
    # are always sufficient.
    for iteration in range(num_vertices - 1):
        # Track whether any distance was improved in this pass.
        # If nothing changed we can stop early — the algorithm has converged.
        any_relaxation_occurred = False

        for (source_vertex, dest_vertex, weight) in graph:
            # Only attempt to relax an edge if the source vertex is reachable.
            if distances[source_vertex] == INFINITY:
                continue

            candidate_distance = distances[source_vertex] + weight

            if candidate_distance < distances[dest_vertex]:
                # A shorter path to dest_vertex has been found.
                distances[dest_vertex] = candidate_distance
                predecessors[dest_vertex] = source_vertex
                any_relaxation_occurred = True

        # Early termination: no relaxation means all shortest paths are final.
        if not any_relaxation_occurred:
            print(f"  [Info] Converged after {iteration + 1} iteration(s) "
                  f"(early stop).")
            break

    # ------------------------------------------------------------------
    # Step 3 – Detect negative-weight cycles
    # ------------------------------------------------------------------
    # If we can still relax an edge after V - 1 passes, there must be a
    # negative-weight cycle reachable from the source.  Such a cycle allows
    # distances to decrease indefinitely, so no finite shortest path exists.
    for (source_vertex, dest_vertex, weight) in graph:
        if distances[source_vertex] == INFINITY:
            continue  # Unreachable vertex — skip

        if distances[source_vertex] + weight < distances[dest_vertex]:
            print(
                "[Warning] Negative-weight cycle detected! "
                "Shortest paths are not well-defined for this graph."
            )
            return None  # Signal failure to the caller

    return distances, predecessors


# ---------------------------------------------------------------------------
# Path reconstruction helper
# ---------------------------------------------------------------------------

def reconstruct_path(
    predecessors: list[int | None],
    source: int,
    target: int,
) -> list[int] | None:
    """Reconstruct the shortest path from *source* to *target*.

    Parameters
    ----------
    predecessors:
        The predecessor array returned by :func:`bellman_ford`.
    source:
        The source vertex used when running Bellman-Ford.
    target:
        The destination vertex whose path we want to reconstruct.

    Returns
    -------
    An ordered list of vertex labels ``[source, …, target]`` representing the
    shortest path, or ``None`` if *target* is unreachable from *source*.
    """

    path: list[int] = []
    current_vertex: int | None = target

    # Walk backwards through the predecessor chain until we reach the source
    # or discover that no path exists.
    while current_vertex is not None:
        path.append(current_vertex)

        if current_vertex == source:
            # We have traced back to the origin — reverse to get source→target.
            path.reverse()
            return path

        current_vertex = predecessors[current_vertex]

    # If we exit the loop without hitting the source, the target is unreachable.
    return None


# ---------------------------------------------------------------------------
# Pretty-printing helpers
# ---------------------------------------------------------------------------

def print_distances(distances: list[float], source: int) -> None:
    """Print a formatted table of shortest distances from the source vertex."""
    print(f"\n{'Vertex':<10} {'Distance from source ' + str(source)}")
    print("-" * 35)
    for vertex, distance in enumerate(distances):
        dist_label = str(distance) if distance != float("inf") else "∞  (unreachable)"
        print(f"  {vertex:<8} {dist_label}")


def print_path(
    predecessors: list[int | None],
    source: int,
    target: int,
    distances: list[float],
) -> None:
    """Print the shortest path and its total cost from source to target."""
    path = reconstruct_path(predecessors, source, target)

    print(f"\nShortest path from vertex {source} to vertex {target}:")
    if path is None:
        print(f"  No path exists — vertex {target} is unreachable.")
    else:
        arrow_path = " → ".join(str(vertex) for vertex in path)
        print(f"  Route : {arrow_path}")
        print(f"  Cost  : {distances[target]}")


# ---------------------------------------------------------------------------
# Entry point with a sample graph
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # ------------------------------------------------------------------
    # Sample graph (directed, weighted — includes a negative edge)
    #
    #        (1)
    #       / | \
    #     6/  |  \5
    #     /  -3   \
    #   (0)   |   (3)
    #     \   |   /
    #     7\  |  /2
    #       \ | /
    #        (2)
    #          \
    #           \-2
    #            (4)
    #
    # Edge list: (from, to, weight)
    # ------------------------------------------------------------------
    sample_edges: list[Edge] = [
        (0, 1,  6),
        (0, 2,  7),
        (1, 2,  8),
        (1, 3,  5),
        (1, 4, -4),
        (2, 3, -3),
        (2, 1,  0),   # 0-weight edge (harmless cycle: round-trip cost ≥ 0)
        (3, 0,  2),
        (4, 3,  7),
    ]

    NUMBER_OF_VERTICES = 5
    SOURCE_VERTEX = 0
    TARGET_VERTEX = 4

    print("=" * 50)
    print("       Bellman-Ford Algorithm Demo")
    print("=" * 50)
    print(f"\nGraph has {NUMBER_OF_VERTICES} vertices and {len(sample_edges)} edges.")
    print(f"Computing shortest paths from source vertex {SOURCE_VERTEX} …\n")

    result = bellman_ford(sample_edges, NUMBER_OF_VERTICES, SOURCE_VERTEX)

    if result is not None:
        shortest_distances, predecessor_map = result
        print_distances(shortest_distances, SOURCE_VERTEX)
        print_path(predecessor_map, SOURCE_VERTEX, TARGET_VERTEX, shortest_distances)
    else:
        print("\nCannot compute shortest paths due to a negative-weight cycle.")

    # ------------------------------------------------------------------
    # Negative cycle demonstration
    # ------------------------------------------------------------------
    print("\n" + "=" * 50)
    print("  Negative-Cycle Detection Demo")
    print("=" * 50)

    negative_cycle_edges: list[Edge] = [
        (0, 1,  1),
        (1, 2, -3),
        (2, 0,  1),   # Round-trip: 1 + (-3) + 1 = -1  ✗  negative cycle!
    ]

    print("\nRunning Bellman-Ford on a graph with a known negative cycle …\n")
    bellman_ford(negative_cycle_edges, num_vertices=3, source=0)
