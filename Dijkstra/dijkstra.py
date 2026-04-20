# ============================================================
#
#   Dijkstra Algoritması — Python Uygulaması
#
#   Açıklama : Ağırlıklı bir grafta, verilen başlangıç
#              düğümünden tüm diğer düğümlere en kısa yolları
#              bulan greedy (açgözlü) algoritma.
#
#   Yapı     : Komşuluk listesi (adjacency list) + Min-Heap
#   Modül    : heapq (Python standart kütüphanesi)
#
#   Yazar    : [Adınız]
#   Tarih    : 2025
#
# ============================================================

import heapq


# ============================================================
#  ANA ALGORİTMA FONKSİYONU
# ============================================================

def dijkstra(graf: dict, başlangıç: str) -> tuple:
    """
    Dijkstra algoritmasını uygular ve en kısa mesafeleri döndürür.

    Parametreler:
    -------------
    graf      : dict
        Komşuluk listesi formatında graf.
        Örnek: {'A': [('B', 4), ('C', 2)], 'B': [('D', 1)], ...}

    başlangıç : str
        Algoritmanın başlayacağı düğümün adı.

    Döndürür:
    ---------
    mesafeler : dict
        Her düğüm için başlangıçtan hesaplanan en kısa mesafe.
        Örnek: {'A': 0, 'B': 3, 'C': 2, 'D': 5}

    öncekiler : dict
        Her düğüme giderken bir önceki düğümü saklar.
        En kısa yolu geri izlemek (trace back) için kullanılır.
        Örnek: {'A': None, 'B': 'C', 'C': 'A', 'D': 'C'}
    """

    # ----------------------------------------------------------
    # ADIM 1: Başlangıç mesafelerini ayarla
    # ----------------------------------------------------------
    # Başlangıç düğümünün mesafesi 0, diğerlerinin sonsuz (∞)
    mesafeler = {düğüm: float('infinity') for düğüm in graf}
    mesafeler[başlangıç] = 0

    # Her düğümün önceki düğümünü None olarak başlat
    # Bu yapı sayesinde hedefe ulaştığımızda tüm yolu geri izleyebiliriz
    öncekiler = {düğüm: None for düğüm in graf}

    # ----------------------------------------------------------
    # ADIM 2: Min-Heap kuyruğunu kur
    # ----------------------------------------------------------
    # Kuyruk elemanları: (toplam_maliyet, düğüm_adı)
    # heapq her zaman en küçük elemanı başa taşır (min-heap)
    kuyruk = [(0, başlangıç)]

    # Hangi düğümlerin kesin olarak çözüldüğünü takip et
    # Bir düğüm kuyruğun başından çıktığında mesafesi finaldir
    ziyaret_edildi = set()

    # ----------------------------------------------------------
    # ADIM 3: Ana döngü
    # ----------------------------------------------------------
    while kuyruk:

        # En düşük maliyetli düğümü kuyruktan çek
        # Bu O(log n) sürer — min-heap'in gücü burada
        mevcut_maliyet, mevcut_düğüm = heapq.heappop(kuyruk)

        # Bu düğümü daha önce işledik mi?
        # Eski bir versiyonu kuyruğa girmiş olabilir; atla
        if mevcut_düğüm in ziyaret_edildi:
            continue

        # Düğümü ziyaret edildi olarak kaydet
        ziyaret_edildi.add(mevcut_düğüm)

        # ----------------------------------------------------------
        # ADIM 4: Komşuları güncelle (Relaxation / Gevşetme)
        # ----------------------------------------------------------
        for komşu, kenar_ağırlığı in graf[mevcut_düğüm]:

            # Bu komşuya bu düğüm üzerinden gelmenin toplam maliyeti
            yeni_maliyet = mevcut_maliyet + kenar_ağırlığı

            # Eğer yeni yol şu ana kadar bilinen yoldan daha ucuzsa:
            if yeni_maliyet < mesafeler[komşu]:

                # Mesafeyi güncelle
                mesafeler[komşu] = yeni_maliyet

                # Hangi düğümden geldiğimizi kaydet (yol izleme için)
                öncekiler[komşu] = mevcut_düğüm

                # Güncel maliyet ile kuyruğa ekle
                # Not: Eski değer hâlâ kuyruktaysa sorun olmaz;
                # ziyaret_edildi seti sayesinde işlendiğinde atlanır
                heapq.heappush(kuyruk, (yeni_maliyet, komşu))

    return mesafeler, öncekiler


# ============================================================
#  YOL GERİ İZLEME FONKSİYONU
# ============================================================

def yolu_geri_izle(öncekiler: dict, başlangıç: str, hedef: str) -> list:
    """
    'öncekiler' sözlüğünü kullanarak başlangıçtan hedefe
    giden tam yolu döndürür.

    Parametreler:
    -------------
    öncekiler : dict
        dijkstra() fonksiyonundan dönen önceki düğüm sözlüğü.

    başlangıç : str
        Yolun başlayacağı düğüm.

    hedef     : str
        Yolun biteceği düğüm.

    Döndürür:
    ---------
    list
        Başlangıçtan hedefe sıralı düğüm listesi.
        Hedefe ulaşılamıyorsa boş liste döner.

    Örnek:
        yolu_geri_izle(öncekiler, 'A', 'D')
        → ['A', 'C', 'D']
    """
    yol = []
    mevcut = hedef

    # Hedef düğüme ulaşılamadıysa (başlangıç hariç) boş liste döndür
    if öncekiler.get(hedef) is None and hedef != başlangıç:
        return []

    # Hedeften başlangıca doğru geriye git
    while mevcut is not None:
        yol.append(mevcut)
        mevcut = öncekiler[mevcut]

    # Ters çevir: başlangıç → hedef
    yol.reverse()
    return yol


# ============================================================
#  YARDIMCI: GÜZEL ÇIKTI FONKSİYONU
# ============================================================

def sonuçları_yazdır(mesafeler: dict, öncekiler: dict, başlangıç: str):
    """
    Dijkstra sonuçlarını düzenli bir tablo olarak yazdırır.
    """
    print("\n" + "=" * 55)
    print(f"  🗺️  Dijkstra Algoritması — Başlangıç Düğümü: '{başlangıç}'")
    print("=" * 55)
    print(f"  {'Hedef':<8} {'Maliyet':>8}   {'En Kısa Yol'}")
    print("-" * 55)

    for düğüm in sorted(mesafeler.keys()):
        maliyet = mesafeler[düğüm]
        yol = yolu_geri_izle(öncekiler, başlangıç, düğüm)

        if maliyet == float('infinity'):
            maliyet_str = "∞ (ulaşılamaz)"
            yol_str = "—"
        else:
            maliyet_str = str(maliyet)
            yol_str = " → ".join(yol)

        print(f"  {düğüm:<8} {maliyet_str:>8}   {yol_str}")

    print("=" * 55 + "\n")


# ============================================================
#  ÖRNEK 1: README'deki Graf
# ============================================================

def örnek_1():
    """
    Basit 4 düğümlü graf:

            4
       A -------> B
       |        / |
       |    1 /   | 5
     2 |    /     |
       |  /    3  |
       C -------> D

    Beklenen çıktı:
      A → A : 0   Yol: A
      A → B : 3   Yol: A → C → B
      A → C : 2   Yol: A → C
      A → D : 5   Yol: A → C → D
    """
    print("\n" + "█" * 55)
    print("  ÖRNEK 1: Basit 4 Düğümlü Graf")
    print("█" * 55)

    graf = {
        'A': [('B', 4), ('C', 2)],
        'B': [('C', 1), ('D', 5)],
        'C': [('D', 3)],
        'D': []
    }

    mesafeler, öncekiler = dijkstra(graf, 'A')
    sonuçları_yazdır(mesafeler, öncekiler, 'A')


# ============================================================
#  ÖRNEK 2: Daha Büyük Bir Şehir Ağı
# ============================================================

def örnek_2():
    """
    6 şehirden oluşan bir yol ağı:

    İstanbul --- 450 --- Ankara
        |                   |
       300                 200
        |                   |
      İzmir --- 550 --- Konya
        |                   |
       400                 350
        |                   |
      Antalya -- 250 -- Adana

    Başlangıç: İstanbul
    """
    print("\n" + "█" * 55)
    print("  ÖRNEK 2: Türkiye Şehir Yol Ağı")
    print("█" * 55)

    şehir_grafı = {
        'İstanbul': [('Ankara', 450), ('İzmir', 300)],
        'Ankara':   [('İstanbul', 450), ('İzmir', 600), ('Konya', 200)],
        'İzmir':    [('İstanbul', 300), ('Ankara', 600), ('Konya', 550), ('Antalya', 400)],
        'Konya':    [('Ankara', 200), ('İzmir', 550), ('Adana', 350)],
        'Antalya':  [('İzmir', 400), ('Adana', 250)],
        'Adana':    [('Konya', 350), ('Antalya', 250)]
    }

    mesafeler, öncekiler = dijkstra(şehir_grafı, 'İstanbul')
    sonuçları_yazdır(mesafeler, öncekiler, 'İstanbul')

    # Belirli bir hedefe yolu ayrıca göster
    hedef = 'Adana'
    yol = yolu_geri_izle(öncekiler, 'İstanbul', hedef)
    print(f"  🎯 İstanbul → {hedef}")
    print(f"     Yol     : {' → '.join(yol)}")
    print(f"     Mesafe  : {mesafeler[hedef]} km\n")


# ============================================================
#  ÖRNEK 3: Bağlantısız Graf (Ulaşılamayan Düğüm)
# ============================================================

def örnek_3():
    """
    İki bileşenli (bağlantısız) graf:

    A --- B --- C     D --- E

    D ve E'ye A'dan ulaşılamaz.
    Bu durumda mesafe ∞ olarak kalmaya devam eder.
    """
    print("\n" + "█" * 55)
    print("  ÖRNEK 3: Bağlantısız Graf")
    print("█" * 55)

    bağlantısız_graf = {
        'A': [('B', 1)],
        'B': [('A', 1), ('C', 2)],
        'C': [('B', 2)],
        'D': [('E', 3)],
        'E': [('D', 3)]
    }

    mesafeler, öncekiler = dijkstra(bağlantısız_graf, 'A')
    sonuçları_yazdır(mesafeler, öncekiler, 'A')


# ============================================================
#  PROGRAMI ÇALIŞTIR
# ============================================================

if __name__ == "__main__":
    örnek_1()
    örnek_2()
    örnek_3()
