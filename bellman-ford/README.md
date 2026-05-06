#  Bellman-Ford Algoritması

> *Negatif ağırlıklı grafiklerde en kısa yolu bulan, döngüleri tespit eden klasik bir algoritma.*

---

##  İçindekiler

1. [Giriş](#1-giriş)
2. [Neden Bellman-Ford?](#2-neden-bellman-ford)
3. [Algoritmanın Mantığı](#3-algoritmanın-mantığı)
4. [Negatif Cycle Nedir?](#4-negatif-cycle-nedir)
5. [Zaman ve Uzay Karmaşıklığı](#5-zaman-ve-uzay-karmaşıklığı)
6. [Kullanım Senaryoları](#6-kullanım-senaryoları)
7. [Python İmplementasyonu](#7-python-i̇mplementasyonu)
8. [Özet](#8-özet)

---

## 1. Giriş

**Bellman-Ford algoritması**, ağırlıklı ve yönlü bir grafik üzerinde tek bir kaynak noktasından diğer tüm köşelere giden **en kısa yolları** bulan bir algoritmadır.

1950'lerin sonunda **Richard Bellman** ve **Lester Ford Jr.** tarafından bağımsız olarak geliştirilen bu algoritma, adını bu iki matematikçiden almaktadır.

### Ne problemi çözer?

Bir şehir haritası düşünün. Kalkış noktanızdan diğer tüm şehirlere olan **en düşük maliyetli** rotaları bulmak istiyorsunuz. Üstelik bazı yolların maliyeti negatif olabilir — örneğin, ürettiğinizden daha fazla enerji kazandıran bir güzergah gibi.

İşte **Bellman-Ford**, bu tür senaryoları başarıyla ele alabilen az sayıdaki algoritmadan biridir.

---

## 2. Neden Bellman-Ford?

### Dijkstra ile Farkı

Pek çok geliştirici ilk olarak **Dijkstra algoritmasını** öğrenir. Dijkstra çok hızlıdır ancak kritik bir kısıtlaması vardır: **negatif ağırlıklı kenarlarla çalışamaz.**

| Özellik | Dijkstra | Bellman-Ford |
|---|---|---|
| Negatif kenar desteği | ❌ | ✅ |
| Negatif döngü tespiti | ❌ | ✅ |
| Zaman karmaşıklığı | O((V + E) log V) | O(V × E) |
| Hız | Daha hızlı | Daha yavaş |

> Dijkstra daha hızlıdır — ama her zaman doğru değildir. Bellman-Ford daha yavaştır — ama daha kapsamlıdır.

### Negatif Ağırlık Neden Önemli?

Gerçek dünyada bazı maliyetler negatif olabilir:

- **Finans:** Arbitraj işlemlerinde bir döviz çevrimi kâr üretebilir.
- **Enerji sistemleri:** Bir güzergah enerji tüketmek yerine enerji kazandırabilir.
- **Oyun geliştirme:** Bir karakter belirli bir yolu geçtiğinde güç veya bonus kazanabilir.

Bu senaryolarda Dijkstra hatalı sonuçlar üretir. Bellman-Ford ise problemi tam anlamıyla çözer.

---

## 3. Algoritmanın Mantığı

### Adım Adım Açıklama

Bellman-Ford, üç temel adımdan oluşur:

**1. Başlatma (Initialization)**

Kaynak köşeye olan mesafe `0`, diğer tüm köşelere olan mesafe `∞` (sonsuz) olarak atanır.

```
distances = [∞, ∞, ∞, ..., ∞]
distances[source] = 0
```

**2. Kenar Gevşetme (Edge Relaxation)**

Tüm kenarlar **V−1 kez** döngüyle taranır. Her kenarda şu kontrol yapılır:

```
Eğer distances[u] + weight(u, v) < distances[v] ise:
    distances[v] = distances[u] + weight(u, v)
    predecessors[v] = u
```

**3. Negatif Döngü Kontrolü**

V−1 iterasyonun ardından kenarlar bir kez daha taranır. Eğer hâlâ bir mesafe güncellenebiliyorsa, grafik **negatif bir döngü** içermektedir.

---

### Relaxation (Gevşetme) Kavramı

**Relaxation**, "bu köşeye giden daha kısa bir yol bulduk mu?" sorusunu soran temel işlemdir.

Şöyle düşünün: A noktasından B noktasına 10 birimlik bir yol biliyorsunuz. Daha sonra A → C → B şeklinde 7 birimlik alternatif bir rota keşfediyorsunuz. Bu durumda B'nin mesafesini **gevşeterek** 10'dan 7'ye güncelliyorsunuz.

Bu işlemi her kenar için, tekrar tekrar uygulamak, en sonunda tüm mesafelerin doğru minimum değere ulaşmasını sağlar.

---

### Neden Tam Olarak V−1 Kez Döner?

Grafikteki herhangi bir **en kısa yol**, bir döngü içermiyorsa en fazla **V−1 kenar** kullanır. Çünkü V adet köşesi olan bir yolda en fazla V−1 adım atılabilir.

Her iterasyonda en az bir köşenin mesafesi kesinleşir. Bu yüzden V−1 iterasyon, tüm kısa yolların bulunması için **yeterli ve gereklidir**.

---

## 4. Negatif Cycle Nedir?

**Negatif cycle (negatif döngü)**, bir grafikteki toplam ağırlığı negatif olan kapalı bir yol döngüsüdür.

### Örnek

```
A → B  (ağırlık: -2)
B → C  (ağırlık: -3)
C → A  (ağırlık: +1)

Döngü toplam ağırlığı: -2 + (-3) + 1 = -4  ❌
```

Bu döngüden ne kadar çok geçilirse toplam maliyet o kadar azalır — sonsuza kadar. Yani **tanımlı bir "en kısa yol" artık mevcut değildir.**

### Neden Problem Oluşturur?

- Algoritma bir türlü yakınsayamaz, mesafeler sürekli küçülür.
- Gerçek dünyada bu durum, finansal sistemlerde **sonsuz arbitraj döngüsü** gibi istenmeyen senaryolara karşılık gelir.
- Bellman-Ford bunu tespit ederek **uyarı verir** ve güvenli biçimde sonlanır.

---

## 5. Zaman ve Uzay Karmaşıklığı

### Zaman Karmaşıklığı

| Durum | Karmaşıklık |
|---|---|
| En kötü durum | **O(V × E)** |
| Erken çıkış ile (en iyi) | **O(E)** |

- **V:** Köşe (vertex) sayısı
- **E:** Kenar (edge) sayısı

V−1 kez tüm kenarlar taranır → `(V-1) × E` işlem yapılır.

### Uzay Karmaşıklığı

| Yapı | Alan |
|---|---|
| `distances` dizisi | **O(V)** |
| `predecessors` dizisi | **O(V)** |
| **Toplam** | **O(V)** |

### Kısa Yorum

Bellman-Ford, büyük ve yoğun grafiklerde yavaş kalabilir. Ancak **negatif kenar içeren** ya da **negatif döngü tespiti gerektiren** durumlarda rakipsizdir. Çoğu pratik uygulamada "erken çıkış" optimizasyonu sayesinde beklenen V−1 iterasyona hiç ulaşılmaz.

---

## 6. Kullanım Senaryoları

Bellman-Ford'un tercih edildiği başlıca alanlar şunlardır:

-  **Ağ yönlendirme protokolleri:** RIP (Routing Information Protocol) doğrudan Bellman-Ford mantığına dayanır.
-  **Döviz arbitrajı tespiti:** Negatif döngü, kâr döngüsü anlamına gelir.
-  **Oyun yapay zekası:** Negatif ağırlıklı hareket maliyetlerini içeren haritalar.
-  **Dağıtık sistemler:** Her düğüm yalnızca komşularıyla iletişim kurduğunda kullanılır.
-  **Biyoinformatik:** Protein etkileşim ağlarında maliyet optimizasyonu.

---

## 7. Python İmplementasyonu

Bu repository, Bellman-Ford algoritmasının **temiz, modüler ve eğitim odaklı** bir Python 3 implementasyonunu içermektedir.

### Dosya: [`bellman_ford.py`](./bellman_ford.py)

İmplementasyon şunları kapsar:

- ✅ Mesafe başlatma
- ✅ Kenar gevşetme (V−1 iterasyon + erken çıkış optimizasyonu)
- ✅ Negatif döngü tespiti
- ✅ En kısa yol yeniden yapılandırma (path reconstruction)
- ✅ Tür ipuçları (type hints) ve docstring'ler
- ✅ PEP 8 uyumlu kod stili

### Hızlı Başlangıç

```bash
# Repoyu klonla
git clone https://github.com/kullanici-adi/bellman-ford.git
cd bellman-ford

# Çalıştır
python bellman_ford.py
```

### Beklenen Çıktı

```
Graph has 5 vertices and 9 edges.

  [Info] Converged after 2 iteration(s) (early stop).

Vertex     Distance from source 0
-----------------------------------
  0        0
  1        6
  2        7
  3        4
  4        2

Shortest path from vertex 0 to vertex 4:
  Route : 0 → 1 → 4
  Cost  : 2
```


## 8. Özet

- 📌 **Bellman-Ford**, negatif ağırlıklı kenarlarla çalışabilen, tek kaynaklı en kısa yol algoritmasıdır.
- 📌 **V−1 iterasyon** yaparak tüm yolları gevşetir; ek bir iterasyonda negatif döngü varlığını tespit eder.
- 📌 Dijkstra'dan **daha yavaştır** ancak Dijkstra'nın çözüm üretemediği grafiklerde **tek geçerli seçenektir.**
- 📌 Ağ yönlendirme, finansal arbitraj tespiti ve dağıtık sistemler gibi **gerçek dünya problemlerinde** aktif olarak kullanılmaktadır.

---
