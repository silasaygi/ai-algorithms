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