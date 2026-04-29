#  Python ile A* (A-Star) Algoritması

> *"En kısa yol her zaman en akıllı yol değildir. Ama en akıllı yol çoğunlukla en kısadır."*

---

##  Giriş — Bir Teslimat Sürücüsünün Sorunu

Sabah 08:00. Bir kargo sürücüsü, şehrin tam ortasındaki depodan kalkıp 12 km ötedeki bir adrese ulaşmak zorunda. Önünde onlarca farklı yol var. Bazıları kısa ama trafik yoğun, bazıları uzun ama akıcı, bazıları ise tamamen kapalı.

GPS'i hangi yolu seçmeli?

Düz bir hesapla tüm yolları denemek saatler alır. İnsan sezgisiyle gitmek ise çoğu zaman yanlış sonuç verir. İşte bu noktada devreye giren algoritma, **A\*** — hedefe ulaşmanın sadece en kısa değil, **en akıllı** yolunu bulan algoritma.

---

##  A\* Algoritması Nedir?

A\* (okunuşu: "A yıldız"), bir **graf arama algoritmasıdır.** İki nokta arasındaki en uygun yolu bulmak için tasarlanmıştır.

Pek çok yol bulma algoritması körü körüne arama yapar — yani hedefe ulaşıp ulaşmadığını umursamadan tüm komşuları sırayla ziyaret eder. A\* ise farklı düşünür:

> *"Şu anki konumum hedefe ne kadar uzak? Buradan devam etmek mantıklı mı?"*

Bu soruyu her adımda soran A\*, gereksiz yönleri budayarak **hedefe odaklı** bir arama yürütür. Bu sayede hem **optimal (en kısa)** hem de **verimli** sonuç üretir.

---

##  Algoritmanın Mantığı

```
f(n) = g(n) + h(n)
```

Bu üç kavramı sezgisel olarak şöyle düşünebilirsiniz:

| Terim | Ne anlama gelir? | Gerçek hayat karşılığı |
|-------|-----------------|------------------------|
| `g(n)` | Başlangıçtan bu noktaya kadar **gerçek maliyet** | "Şimdiye kadar kaç adım attım?" |
| `h(n)` | Bu noktadan hedefe kadar **tahmini maliyet** | "Hedefe daha ne kadar kaldı (tahminim)?" |
| `f(n)` | Toplam tahmini maliyet | "Bu yolu seçersem toplam ne kadar sürer?" |

Algoritma her adımda **en düşük `f(n)` değerine** sahip düğümü seçer ve oradan devam eder. Bu sayede hem geride ne kadar yol kat ettiğini hem de önde ne kadar yol kaldığını dengeleyerek ilerler.

###  Heuristic (Sezgisel Fonksiyon) Nedir?

`h(n)`, **tahmini** bir değerdir — gerçeği değil, en iyi tahmini temsil eder. Bu tahminin nasıl yapıldığını belirleyen fonksiyona **heuristic** (sezgisel fonksiyon) denir.

Heuristic'in altın kuralı: **Gerçek maliyeti asla fazla tahmin etmemek.** Buna "kabul edilebilir" (admissible) heuristic denir ve bu kural sağlandığında A\* her zaman **optimal yolu** bulur.

###  Manhattan Mesafesi

Bu projede **4 yönlü hareket** kullanıldığından (yukarı, aşağı, sol, sağ — çapraz yok) heuristic olarak **Manhattan Mesafesi** seçilmiştir:

```
h = |mevcut_satır - hedef_satır| + |mevcut_sütun - hedef_sütun|
```

Adını New York'un ızgara şeklindeki sokak planından alır. Çapraz geçişin olmadığı bir şehirde iki nokta arasındaki minimum adım sayısını verir — ne fazla, ne eksik.

##  Gerçek Hayat Kullanım Alanları

A\* soyut bir algoritma değil — gündelik hayatın içinde:

-  **Navigasyon:** Google Haritalar ve GPS sistemleri, araç rotası hesaplarken A\*'a benzer algoritmalar kullanır
-  **Video Oyunları:** Oyun haritalarında NPC'lerin (oyuncu olmayan karakterlerin) engelleri aşarak hedefe ulaşması A\* ile sağlanır
-  **Robotik:** Otonom robotlar ve insansız araçlar, fiziksel ortamda güvenli rota planlamak için A\*'ı temel alır
-  **Lojistik ve Depo Yönetimi:** Amazon gibi şirketlerin depo robotları raflar arasındaki en verimli yolu A\* ile hesaplar
-  **Yapay Zeka Bulmacaları:** 8-puzzle, 15-puzzle gibi klasik yapay zeka problemleri A\* ile çözülür

---

### Izgara Yapısı


```python
GRID = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0],
]
```

| Değer | Anlamı |
|-------|--------|
| `0` | Geçilebilir hücre |
| `1` | Engel (duvar) |

### Engel Mantığı

`is_valid()` fonksiyonu her komşu düğüm için iki kontrol yapar: hücre ızgara sınırları içinde mi? Ve değeri `1` (engel) değil mi? Bu iki koşul sağlanmazsa o yön göz ardı edilir.

### Yol Bulma Süreci

1. Başlangıç düğümü öncelik kuyruğuna eklenir
2. En düşük `f(n)` değerli düğüm kuyruktan çıkarılır
3. Bu düğümün 4 komşusu incelenir
4. Her geçerli komşu için `g`, `h` ve `f` değerleri hesaplanır
5. Daha ucuz bir yol bulunursa komşu güncellenir ve kuyruğa eklenir
6. Hedefe ulaşıldığında `came_from` haritası geriye izlenerek yol yeniden oluşturulur

---

##  Örnek Çalışma

**Başlangıç:** `(0, 0)` — sol üst köşe  
**Hedef:** `(5, 6)` — sağ alt köşe

```
Yol bulmadan önce:

  │S . . . . . . │
  │. # # # . # . │
  │. . . # . # . │
  │. # . . . . . │
  │. # # # # # . │
  │. . . . . . G │
```

```
A* çalıştırıldıktan sonra:

  │S * * * * * * │
  │. # # # . # * │
  │. . . # . # * │
  │. # . . . . * │
  │. # # # # # * │
  │. . . . . . G │

  S=Başlangıç  G=Hedef  *=Yol  #=Engel  .=Boş
```

Algoritma engel duvarını aşmak için önce sağa, ardından aşağıya inerek **11 adımlık en kısa yolu** bulur.

---


##  Çıktı Açıklaması

Program çalıştığında sırasıyla şunları görürsünüz:

**1. Özet bilgi**
```
Start : (0, 0)
Goal  : (5, 6)
Grid  : 6 satır × 7 sütun
```

**2. Sonuç ve koordinat listesi**
```
✓ En kısa yol bulundu!  Uzunluk = 11 adım

Yol: (0,0) → (0,1) → (0,2) → (0,3) → (0,4) → (0,5) → (0,6)
          → (1,6) → (2,6) → (3,6) → (4,6) → (5,6)
```

**3. Görsel ızgara** — yukarıdaki gibi `*` ile işaretlenmiş yol

**4. Adım adım maliyet tablosu**
```
Adım   Düğüm         g      h      f
──────────────────────────────────────
0      (0, 0)        0     11     11   ← başlangıç
1      (0, 1)        1     10     11
2      (0, 2)        2      9     11
...
11     (5, 6)       11      0     11   ← hedef
```

> Bu tablodaki `f` değerinin sabit kalması, A\*'ın hedefe dik bir çizgi üzerinde ilerlediğinin ve sezgisel fonksiyonun mükemmel çalıştığının göstergesidir.

Eğer yol bulunamazsa program şu mesajı verir:
```
✗ Yol bulunamadı — hedef erişilemez durumda.
```

## Sonuç

A* algoritması bize şunu gösterir:  
Doğru çözüme ulaşmak, sadece çok çalışmakla değil, **doğru yönde ilerlemekle** ilgilidir.

Bazen tüm yolları denemek yerine,  
nereye gittiğini bilen bir yaklaşım çok daha değerlidir :)

---

*Projeyi faydalı bulduysanız ⭐ vermeyi unutmayın — destekleriniz için teşekkür ediyorum.*
