"""
================================================
  Depth-First Search (DFS) — Derinlemesine Arama
================================================

  İçerik:
    1. Recursive DFS
    2. Iterative DFS  (stack tabanlı)
    3. DFS — tüm yolları bul
    4. DFS — döngü tespiti
    5. DFS — topolojik sıralama
    6. Örnek çalıştırma
================================================
"""

from collections import defaultdict


# ─────────────────────────────────────────────
# Yardımcı: Graf oluşturucu
# ─────────────────────────────────────────────

class Graph:
    """Yönlü veya yönsüz adjacency-list graf."""

    def __init__(self, directed: bool = False):
        self.graph: dict[int, list[int]] = defaultdict(list)
        self.directed = directed

    def add_edge(self, u: int, v: int) -> None:
        self.graph[u].append(v)
        if not self.directed:
            self.graph[v].append(u)

    def __repr__(self) -> str:
        lines = [f"  {node}: {neighbors}" for node, neighbors in sorted(self.graph.items())]
        return "Graph {\n" + "\n".join(lines) + "\n}"


# ─────────────────────────────────────────────
# 1. Recursive DFS
# ─────────────────────────────────────────────

def dfs_recursive(
    graph: dict,
    node: int,
    visited: set | None = None,
    order: list | None = None,
) -> list[int]:
    """
    Özyinelemeli DFS.

    Args:
        graph  : Komşuluk listesi  {düğüm: [komşular]}
        node   : Başlangıç düğümü
        visited: Ziyaret edilen düğümler seti (dahili)
        order  : Ziyaret sırası listesi (dahili)

    Returns:
        Ziyaret sırası listesi
    """
    if visited is None:
        visited = set()
    if order is None:
        order = []

    visited.add(node)
    order.append(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited, order)

    return order


# ─────────────────────────────────────────────
# 2. Iterative DFS  (stack tabanlı)
# ─────────────────────────────────────────────

def dfs_iterative(graph: dict, start: int) -> list[int]:
    """
    Stack kullanarak iterative DFS.
    Büyük graflarda recursive'in stack overflow riskini ortadan kaldırır.

    Args:
        graph : Komşuluk listesi
        start : Başlangıç düğümü

    Returns:
        Ziyaret sırası listesi
    """
    visited = set()
    stack   = [start]
    order   = []

    while stack:
        node = stack.pop()          # LIFO — en son eklenen ilk çıkar

        if node in visited:
            continue

        visited.add(node)
        order.append(node)

        # Komşuları ters sırayla ekle → doğal sırada pop edilsin
        for neighbor in reversed(graph[node]):
            if neighbor not in visited:
                stack.append(neighbor)

    return order


# ─────────────────────────────────────────────
# 3. DFS — başlangıçtan hedefe tüm yollar
# ─────────────────────────────────────────────

def dfs_all_paths(
    graph: dict,
    start: int,
    end: int,
    path: list | None = None,
    all_paths: list | None = None,
) -> list[list[int]]:
    """
    Başlangıç düğümünden hedef düğüme ulaşan tüm yolları bulur.

    Args:
        graph    : Komşuluk listesi
        start    : Başlangıç düğümü
        end      : Hedef düğüm
        path     : Anlık yol (dahili)
        all_paths: Tüm yollar (dahili)

    Returns:
        Bulunan tüm yolların listesi
    """
    if path is None:
        path = []
    if all_paths is None:
        all_paths = []

    path = path + [start]           # Kopyala — backtrack için orijinali koru

    if start == end:
        all_paths.append(path)
        return all_paths

    for neighbor in graph[start]:
        if neighbor not in path:    # Döngüye girme
            dfs_all_paths(graph, neighbor, end, path, all_paths)

    return all_paths


# ─────────────────────────────────────────────
# 4. DFS — döngü tespiti (yönlü graf)
# ─────────────────────────────────────────────

def dfs_has_cycle(graph: dict, nodes: list[int]) -> bool:
    """
    Yönlü grafta döngü olup olmadığını tespit eder.
    "Gri" (işlenmekte olan) düğüme tekrar ulaşılırsa döngü vardır.

    Args:
        graph : Komşuluk listesi
        nodes : Graftaki tüm düğümler

    Returns:
        True → döngü var, False → döngü yok
    """
    WHITE, GRAY, BLACK = 0, 1, 2    # İşlenmemiş / İşleniyor / Tamamlandı
    color = {node: WHITE for node in nodes}

    def dfs(node: int) -> bool:
        color[node] = GRAY           # Ziyaret başladı

        for neighbor in graph[node]:
            if color[neighbor] == GRAY:     # Kendine ya da ataya geri döndü
                return True
            if color[neighbor] == WHITE:
                if dfs(neighbor):
                    return True

        color[node] = BLACK          # Ziyaret tamamlandı
        return False

    for node in nodes:
        if color[node] == WHITE:
            if dfs(node):
                return True

    return False


# ─────────────────────────────────────────────
# 5. DFS — topolojik sıralama (yönlü asiklik graf)
# ─────────────────────────────────────────────

def dfs_topological_sort(graph: dict, nodes: list[int]) -> list[int]:
    """
    Yönlü asiklik grafta (DAG) topolojik sıralama yapar.
    Kullanım: bağımlılık çözümü, derleme sırası, görev planlama.

    Args:
        graph : Komşuluk listesi
        nodes : Graftaki tüm düğümler

    Returns:
        Topolojik sıralanmış düğüm listesi

    Raises:
        ValueError: Graf döngü içeriyorsa
    """
    if dfs_has_cycle(graph, nodes):
        raise ValueError("Graf döngü içeriyor — topolojik sıralama yapılamaz.")

    visited = set()
    stack   = []

    def dfs(node: int) -> None:
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)           # Tüm komşular bittikten sonra ekle

    for node in nodes:
        if node not in visited:
            dfs(node)

    return stack[::-1]              # Ters çevir → doğru sıra


# ─────────────────────────────────────────────
# 6. Örnek çalıştırma
# ─────────────────────────────────────────────

def _separator(title: str) -> None:
    print(f"\n{'─' * 45}")
    print(f"  {title}")
    print(f"{'─' * 45}")


def main() -> None:

    # ── Graf 1: Yönsüz ──────────────────────
    #
    #     1
    #    / \
    #   2   3
    #  / \
    # 4   5
    #
    g1 = Graph(directed=False)
    for u, v in [(1, 2), (1, 3), (2, 4), (2, 5)]:
        g1.add_edge(u, v)

    _separator("Graf 1 — Yönsüz")
    print(g1)

    print("\n[Recursive DFS]  başlangıç=1")
    print("Ziyaret sırası:", dfs_recursive(g1.graph, 1))

    print("\n[Iterative DFS]  başlangıç=1")
    print("Ziyaret sırası:", dfs_iterative(g1.graph, 1))

    print("\n[Tüm yollar]  1 → 4")
    for path in dfs_all_paths(g1.graph, 1, 4):
        print(" →".join(map(str, path)))

    # ── Graf 2: Yönlü, döngüsüz (DAG) ──────
    #
    #  A(1) → B(2) → D(4)
    #    \         ↗
    #     C(3) ──
    #
    _separator("Graf 2 — Yönlü DAG (topolojik sıralama)")
    g2 = Graph(directed=True)
    for u, v in [(1, 2), (1, 3), (2, 4), (3, 4)]:
        g2.add_edge(u, v)
    print(g2)

    nodes_g2 = [1, 2, 3, 4]
    print("\n[Döngü tespiti]")
    print("Döngü var mı?", dfs_has_cycle(g2.graph, nodes_g2))

    print("\n[Topolojik sıralama]")
    print("Sıra:", dfs_topological_sort(g2.graph, nodes_g2))

    # ── Graf 3: Yönlü, döngülü ──────────────
    #
    #  1 → 2 → 3
    #  ↑       |
    #  └───────┘
    #
    _separator("Graf 3 — Yönlü, döngülü")
    g3 = Graph(directed=True)
    for u, v in [(1, 2), (2, 3), (3, 1)]:
        g3.add_edge(u, v)
    print(g3)

    nodes_g3 = [1, 2, 3]
    print("\n[Döngü tespiti]")
    print("Döngü var mı?", dfs_has_cycle(g3.graph, nodes_g3))

    try:
        dfs_topological_sort(g3.graph, nodes_g3)
    except ValueError as e:
        print(f"[Topolojik sıralama] Hata → {e}")


if __name__ == "__main__":
    main()