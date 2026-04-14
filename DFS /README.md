# DFS (Depth-First Search) Algoritması

##  İçindekiler

- [Giriş](#giriş)
- [DFS Nedir?](#dfs-nedir)
- [Adım Adım Örnek](#adım-adım-örnek)
- [Algoritmanın Temel Bileşenleri](#algoritmanın-temel-bileşenleri)
- [Karmaşıklık Analizi](#karmaşıklık-analizi)
- [DFS Ne Zaman Tercih Edilir?](#dfs-ne-zaman-tercih-edilir)
- [Sonuç](#sonuç)
---

##  Giriş

Depth-First Search (DFS), graf veri yapılarında gezinme ve arama için kullanılan temel algoritmalardan biridir.  

Bu algoritma, bir başlangıç düğümünden başlayarak graf üzerinde **olabildiğince derine inerek** ilerler ve çıkmaz bir noktaya ulaştığında geri dönerek diğer yolları keşfeder.

---

##  DFS Nedir?

DFS, bir graf üzerinde gezinirken **derinlik öncelikli** bir strateji izler:

- Başlangıç düğümünü ziyaret eder  
- Bir komşuya gider ve **olabildiğince derine iner**  
- Daha fazla ilerleyemediğinde geri döner (*backtracking*)  
- Alternatif yolları keşfetmeye devam eder  

> **Anahtar Özellik:** DFS, bir yolu sonuna kadar keşfetmeden diğerine geçmez.

---

## Adım Adım Örnek

### Graf Yapısı

```
    1
   / \
  2   3
 / \
4   5
```

```python
graph = {
    1: [2, 3],
    2: [4, 5],
    3: [],
    4: [],
    5: []
}
```

### DFS Adımları (`başlangıç = 1`)

| Adım | Ziyaret Edilen | Stack | Açıklama |
|------|---------------|-------|----------|
| 1 | `1` | `[2, 3]` | 1'den başla, komşuları stack'e ekle |
| 2 | `1 → 2` | `[4, 5, 3]` | Stack'ten 2'yi al, komşuları ekle |
| 3 | `1 → 2 → 4` | `[5, 3]` | Stack'ten 4'ü al, komşusu yok |
| 4 | `1 → 2 → 4 → 5` | `[3]` | Stack'ten 5'i al, komşusu yok |
| 5 | `1 → 2 → 4 → 5 → 3` | `[]` | Stack'ten 3'ü al, komşusu yok. Bitti! |

> **Sonuç:** `1 → 2 → 4 → 5 → 3`


##  Algoritmanın Temel Bileşenleri

---

### 1. Recursive (Özyinelemeli) Versiyon

def dfs_recursive(graph, node, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(node)
    print(node, end=" ")
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)
    
    return visited


Nasıl çalışıyor? Python'un kendi call stack'i bizim için backtracking'i otomatik halleder. dfs_recursive(graph, 2, ...) çağrısı bitmeden 3'e geçilmez. Fonksiyon kendini çağırır, derine iner, biter, geri döner.

---

### 2. Iterative (Stack Kullanan) Versiyon
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()

        if node in visited:
            continue

        visited.add(node)
        print(node, end=" ")

        for neighbor in reversed(graph[node]):
            stack.append(neighbor)

---
## ⏱️ Karmaşıklık Analizi (Big-O)

| Tür | Notasyon | Açıklama |
|-----|----------|----------|
| **Zaman** | `O(V + E)` | V = vertex (düğüm sayısı), E = edge (kenar sayısı). Her düğüme ve her kenara yalnızca **bir kez** bakılır. |
| **Uzay (Iterative)** | `O(V)` | Stack ve `visited` seti en fazla V eleman tutar. |
| **Uzay (Recursive)** | `O(V)` | `visited` seti + Python'un call stack'i. Zincir grafta derinlik V'ye ulaşabilir. |


---

## DFS Ne Zaman Tercih Edilir?
DFS'i seç, eğer:

Belirli bir yol var mı? sorusuna cevap arıyorsan (labirent, bağlantı kontrolü)
Graf üzerinde döngü tespiti yapman gerekiyorsa
Topolojik sıralama yapman gerekiyorsa (bağımlılık çözümü, derleme sırası)
Tüm kombinasyonları ya da tüm yolları keşfetmen gerekiyorsa (backtracking problemleri: sudoku, N-queens)
Bellek sınırın dar, ama grafın çok geniş olduğu durumlarda (BFS geniş grafta muazzam bellek yer)

BFS'i seç, eğer:

En kısa yolu bulmak istiyorsan (ağırlıksız graflarda)
Cevabın başlangıca yakın olduğunu biliyorsan
Seviye seviye (katman katman) işlem yapman gerekiyorsa

---

## Sonuç

Bu yaklaşım yalnızca bir arama yöntemi değil, aynı zamanda birçok önemli problemin çözüm mantığının temelidir.
Backtracking, topolojik sıralama ve yol arama gibi konuların arkasında hep bu düşünce vardır.
