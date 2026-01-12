# BFS (Breadth-First Search) Algoritması 

## İçindekiler
- [Giriş](#giriş)
- [BFS Nedir?](#bfs-nedir)
- [Algoritmanın Temel Bileşenleri](#algoritmanın-temel-bileşenleri)
- [Çalışma Mantığı](#çalışma-mantığı)
- [Kod Analizi](#kod-analizi)
- [Adım Adım Örnek](#adım-adım-örnek)
- [Zaman ve Alan Karmaşıklığı](#zaman-ve-alan-karmaşıklığı)
- [Kullanım Alanları](#kullanım-alanları)

---

## Giriş

Breadth-First Search (BFS), graf veri yapılarında gezinme ve arama için kullanılan temel algoritmalardan biridir. Bu algoritma, bir başlangıç düğümünden başlayarak grafiği **katman katman** (seviye seviye) gezer.

---

## BFS Nedir?

BFS, bir graf üzerinde gezinirken **genişlik öncelikli** bir strateji izler. Yani:

- Önce başlangıç düğümünü ziyaret eder
- Sonra başlangıç düğümünün **tüm komşularını** ziyaret eder
- Ardından bu komşuların komşularını ziyaret eder
- Bu işlem tüm erişilebilir düğümler gezilene kadar devam eder

**Anahtar Özellik:** BFS, düğümleri başlangıç noktasına olan **uzaklıklarına göre** sırayla ziyaret eder.

---

## Algoritmanın Temel Bileşenleri

### 1. **Queue (Kuyruk) - FIFO Yapısı**
```python
queue = deque()
```
- İlk giren ilk çıkar (First-In, First-Out) mantığıyla çalışır
- Ziyaret edilecek düğümleri sırayla tutar
- `popleft()` ile kuyruğun başından düğüm alırız
- `append()` ile kuyruğun sonuna düğüm ekleriz

### 2. **Visited Set (Ziyaret Edilen Düğümler)**
```python
visited_set = set()
```
- Daha önce ziyaret ettiğimiz düğümleri takip eder
- Aynı düğümü birden fazla kez işlememizi engeller
- Sonsuz döngüleri önler
- Hızlı arama için `set` veri yapısı kullanılır (O(1) arama)

### 3. **Graph (Graf) - Adjacency List**
```python
my_graph = {
    'A': ['B', 'E', 'F'],
    'B': ['A', 'C'],
    # ...
}
```
- Graf, komşuluk listesi (adjacency list) olarak temsil edilir
- Her düğüm için komşuları bir liste halinde tutulur

---

## Çalışma Mantığı

BFS algoritması şu adımları izler:

1. **Başlangıç düğümünü işaretle ve kuyruğa ekle**
   - Başlangıç düğümü `visited_set`'e eklenir
   - Aynı düğüm `queue`'ya eklenir

2. **Kuyruk boş olana kadar döngü**
   - Kuyruktan bir düğüm çıkar (`popleft()`)
   - Bu düğümle istenen işlemi yap (yazdır, kaydet, vb.)

3. **Komşuları kontrol et**
   - Çıkarılan düğümün tüm komşularını incele
   - Henüz ziyaret edilmemiş komşuları bul

4. **Yeni düğümleri işaretle ve kuyruğa ekle**
   - Ziyaret edilmemiş her komşu `visited_set`'e eklenir
   - Aynı komşular `queue`'ya eklenir

5. **Tekrarla**
   - Kuyruk boşalana kadar adımlar tekrarlanır

---

## Kod Analizi

```python
def bfs(graph, start_node):
    # Kuyruk yapısı oluştur (FIFO)
    queue = deque()
    
    # Ziyaret edilen düğümleri takip et
    visited_set = set()
    
    # Başlangıç düğümünü işaretle
    visited_set.add(start_node)
    
    # Başlangıç düğümünü kuyruğa ekle
    queue.append(start_node)
    
    # Kuyruk boş olana kadar devam et
    while queue:
        # Kuyruğun başındaki düğümü al
        current_node = queue.popleft()
        
        # Düğümle işlem yap (örn: yazdır)
        print(current_node)
        
        # Mevcut düğümün tüm komşularını kontrol et
        for neighbor in graph[current_node]:
            # Sadece daha önce ziyaret edilmemiş komşuları işle
            if neighbor not in visited_set:
                # Komşuyu ziyaret edildi olarak işaretle
                visited_set.add(neighbor)
                
                # Komşuyu kuyruğa ekle
                queue.append(neighbor)
```

---

## Adım Adım Örnek

Verilen graf yapısı:
```
    A
   /|\
  B E F
  |   |
  C   I
 /|   |
G D   |
  |   |
  H   |
   \ /
    E-F
```

### Çalıştırma: `bfs(my_graph, 'A')`

**İlk Durum:**
- Queue: `[A]`
- Visited: `{A}`

**Adım 1:** A'yı işle
- Current: `A`
- Komşular: `B, E, F` → Hepsi yeni, kuyruğa ekle
- Queue: `[B, E, F]`
- Visited: `{A, B, E, F}`

**Adım 2:** B'yi işle
- Current: `B`
- Komşular: `A, C` → A zaten ziyaret edildi, sadece C ekle
- Queue: `[E, F, C]`
- Visited: `{A, B, E, F, C}`

**Adım 3:** E'yi işle
- Current: `E`
- Komşular: `A, I` → A zaten var, sadece I ekle
- Queue: `[F, C, I]`
- Visited: `{A, B, E, F, C, I}`

**Adım 4:** F'yi işle
- Current: `F`
- Komşular: `A, I` → İkisi de zaten var
- Queue: `[C, I]`
- Visited: `{A, B, E, F, C, I}`

**Adım 5:** C'yi işle
- Current: `C`
- Komşular: `B, D, G` → B var, D ve G ekle
- Queue: `[I, D, G]`
- Visited: `{A, B, E, F, C, I, D, G}`

**Adım 6:** I'yı işle
- Current: `I`
- Komşular: `E, F` → İkisi de var
- Queue: `[D, G]`

**Adım 7:** D'yi işle
- Current: `D`
- Komşular: `C, H` → C var, H ekle
- Queue: `[G, H]`
- Visited: `{A, B, E, F, C, I, D, G, H}`

**Adım 8-9:** G ve H işlenir
- Queue boşalır
- Tüm düğümler ziyaret edilmiştir

**Çıktı Sırası:** `A → B → E → F → C → I → D → G → H`

---

## Zaman ve Alan Karmaşıklığı

### Zaman Karmaşıklığı: **O(V + E)**
- **V**: Düğüm (vertex) sayısı
- **E**: Kenar (edge) sayısı
- Her düğüm bir kez ziyaret edilir: O(V)
- Her kenar bir kez kontrol edilir: O(E)

### Alan Karmaşıklığı: **O(V)**
- Queue'da en fazla V düğüm tutulabilir
- Visited set'te V düğüm saklanır

---

## Kullanım Alanları

BFS algoritması birçok alanda kullanılır:

 **En Kısa Yol Bulma** - Ağırlıksız graflarda iki düğüm arası en kısa yol

 **Sosyal Ağ Analizi** - Bağlantı dereceleri, arkadaş önerileri

 **Web Crawler** - Web sayfalarını seviye seviye tarama

 **Ağ Broadcast** - Tüm bağlı cihazlara mesaj gönderme

 **Labirent Çözme** - En kısa çıkış yolunu bulma

 **Bağlantılı Bileşenler** - Grafta kopuk parçaları bulma

 **GPS Navigasyon** - Şehir haritalarında rota bulma

---

## Sonuç

BFS, graf algoritmalarının temel taşlarından biridir. Kuyruk yapısı sayesinde düğümleri seviye seviye gezerek, başlangıç noktasına en yakın düğümlerden başlayıp giderek uzaklaşır. Bu özellik, onu en kısa yol problemleri için ideal bir seçim haline getirir.
