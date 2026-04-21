#  Dijkstra Algoritması — En Kısa Yol Problemi

## İçindekiler

- [Giriş](#-giriş)
- [Problem Tanımı](#-problem-tanımı)
- [Dijkstra Nasıl Çalışır?](#-dijkstra-nasıl-çalışır)
- [Adım Adım Görselleştirme](#-adım-adım-görselleştirme)
- [Zaman ve Alan Karmaşıklığı](#-zaman-ve-alan-karmaşıklığı)
- [Avantajlar ve Sınırlamalar](#-avantajlar-ve-sınırlamalar)
- [Sonuç](#-sonuç)

---

## Giriş

Elinizde bir şehir haritası olduğunu hayal edin. A noktasından B noktasına gitmek istiyorsunuz. Birden fazla yol var ve her yolun farklı bir mesafesi (ya da maliyeti) mevcut. Peki **en kısa yolu** nasıl bulursunuz?

İşte bu soruyu 1956 yılında Hollandalı bilgisayar bilimcisi **Edsger W. Dijkstra** yanıtladı. Kendi adıyla anılan bu algoritma, **ağırlıklı bir grafta** bir kaynak düğümden diğer tüm düğümlere giden **en kısa yolları** bulan bir arama algoritmasıdır.

### Neden Önemlidir?

Dijkstra Algoritması, bilgisayar biliminin temel taşlarından biridir çünkü:

- **Google Maps, Waze, Apple Maps** gibi navigasyon uygulamalarının altında yatan temel mantığı oluşturur.
- **İnternet yönlendirme protokolleri** (OSPF gibi) paketleri en verimli yoldan iletmek için bu algoritmayı kullanır.
- **Oyun yapay zekâsı**, karakterlerin harita üzerinde en hızlı yolu bulmasını sağlar.
- Lojistik, tedarik zinciri, uçuş güzergâhı planlaması gibi onlarca alanda aktif olarak kullanılmaktadır.

Dijkstra'yı anlamak, yalnızca bir algoritmayı öğrenmek değil; **problem çözme düşüncenizi** temelden geliştirmektir.

---

## Problem Tanımı

### En Kısa Yol Problemi Nedir?

Bir grafın düğümler (nodes/vertices) ve kenarlardan (edges) oluştuğunu düşünelim. Her kenarın bir **ağırlığı** (weight) vardır — bu mesafe, zaman, maliyet veya başka bir ölçüt olabilir.

**En Kısa Yol Problemi:** Verilen bir başlangıç düğümünden, graftaki diğer tüm düğümlere ulaşmak için geçilmesi gereken **minimum toplam maliyetli yolu** bulmaktır.

---
## Dijkstra Nasıl Çalışır?

Algoritmanın temel fikri son derece sezgiseldir:

> **"Her seferinde, şimdiye kadar ulaşabileceğimiz en ucuz düğümü ziyaret et ve onun komşularını güncelle."**

### Adım Adım Mantık Akışı

**1. Başlangıç:**
- Başlangıç düğümünün mesafesini `0` olarak ayarla.
- Diğer tüm düğümlerin mesafesini `sonsuz (∞)` olarak ayarla.
- Tüm düğümleri "henüz ziyaret edilmedi" olarak işaretle.
- Başlangıç düğümünü bir **öncelik kuyruğuna (min-heap)** ekle.

**2. Ana Döngü:**
- Öncelik kuyruğundan **en düşük maliyetli** düğümü çıkar.
- Bu düğüm zaten ziyaret edildiyse atla.
- Bu düğümü "ziyaret edildi" olarak işaretle.
- Komşularının her biri için:
  - `yeni_maliyet = mevcut_düğüm_maliyeti + kenar_ağırlığı`
  - Eğer `yeni_maliyet < komşunun_şimdiki_maliyeti` ise güncelle ve kuyruğa ekle.

**3. Bitiş:**
- Kuyruk boşaldığında algoritma tamamdır.
- Her düğüm için hesaplanan mesafe, başlangıç noktasından o düğüme giden **en kısa mesafedir.**

---

##  Zaman ve Alan Karmaşıklığı

### Zaman Karmaşıklığı

| Yapı | Karmaşıklık | Açıklama |
|------|-------------|----------|
| Min-Heap + Komşuluk Listesi | **O((V + E) log V)** | En yaygın kullanılan versiyon |
| Fibonacci Heap ile | O(E + V log V) | Teorik optimum, pratikte nadiren kullanılır |
| Basit dizi ile | O(V²) | Küçük graflar için kabul edilebilir |

Burada `V` = düğüm (vertex) sayısı, `E` = kenar (edge) sayısıdır.

### Sezgisel Açıklama

- **Her düğümü en fazla bir kez** kuyruğa ekliyoruz → `V` işlem.
- **Her kenarı en fazla bir kez** kontrol ediyoruz → `E` işlem.
- **Heap'ten çekme/ekleme** işlemi `O(log V)` alır.
- Toplamda: `O((V + E) × log V)`

**Pratikte ne anlama gelir?**  
1000 düğümlü, 5000 kenarlı bir grafta yaklaşık `6000 × 10 = 60.000` temel işlem yapılır. Bu inanılmaz derecede hızlıdır!

### Alan Karmaşıklığı

| Yapı | Alan | Açıklama |
|------|------|----------|
| Mesafe sözlüğü | O(V) | Her düğüm için bir değer |
| Önceki düğüm sözlüğü | O(V) | Yol izleme için |
| Min-Heap (kuyruk) | O(V) | En kötü durumda tüm düğümler |
| **Toplam** | **O(V + E)** | Komşuluk listesi dahil |


---

## Avantajlar ve Sınırlamalar

### Avantajlar

- **Doğruluğu garanti:** Ağırlıklar negatif olmadığı sürece her zaman gerçek en kısa yolu bulur.
- **Verimlilik:** `O((V+E) log V)` ile büyük grafları rahatlıkla işler.
- **Tüm yolları hesaplar:** Tek çalıştırmada başlangıç düğümünden tüm düğümlere olan mesafeler elde edilir.
- **Anlaşılması kolay:** Sezgisel ve uygulaması görece basittir.
- **Geniş uygulama alanı:** Onlarca gerçek dünya problemine uyarlanabilir.

### Sınırlamalar

- **Negatif ağırlıklarla çalışmaz:** Negatif kenarlı graflarda yanlış sonuç verir. Bu durumda **Bellman-Ford** algoritması kullanılmalıdır.
- **Dinamik graflarda yetersiz:** Ağırlıklar sık değişirse her seferinde yeniden çalıştırmak gerekir. Bu durumda **D\* Lite** gibi algoritmalar tercih edilir.
- **Büyük graflarda bellek:** Tüm düğümleri saklamak çok büyük ağlarda bellek sorununa yol açabilir.
- **Yön bilgisi yoktur:** Düz Dijkstra, hedefe yönelimli değildir; tüm yönlere eşit "yayılır". Bu yüzden A\* gibi sezgisel (heuristic) algoritmalar büyük haritalarda daha hızlı olabilir.

---

## Sonuç

Dijkstra Algoritması, bilgisayar biliminin en zarif ve kullanışlı buluşlarından biridir.
1956'dan bu yana navigasyondan ağ protokollerine, oyun geliştirmeden biyoinformatiğe kadar sayısız alanda temel bir araç olarak kullanılmaya devam etmektedir.

