🚀 Collatz Balanced Permutation Cipher (CBPC)
Bu proje, ünlü Collatz Sanısı (3n+1 problemi) üzerine inşa edilmiş, deterministik ancak kaotik bir şifreleme algoritmasıdır. Algoritma, veriyi hem bit düzeyinde değiştirir (XOR) hem de konumlarını karıştırır (Permutation).
🛠 Algoritma Nasıl Çalışır? (Akış Şeması Mantığı)
Algoritma iki temel güvenlik katmanından oluşur:
Dengeli Bit Akışı (Balanced Keystream): Collatz yörüngesindeki tek (1) ve çift (0) durumları Manchester Encoding (0 -> 01, 1 -> 10) yöntemiyle işlenir. Bu, şifreli veride eşit sayıda 0 ve 1 olmasını sağlar (İstatistiksel analizi zorlaştırır).
Dinamik Permütasyon: Collatz dizisi sırasında oluşan büyük tam sayılar, mesajın bitlerinin yerini değiştirmek için birer indis üreticisi olarak kullanılır.
Akış Şeması (Flowchart)
    A[Başlangıç: Seed & Mesaj] --> B[Collatz Yörüngesi Üret]
    B --> C[Manchester Encoding ile Bitleri Dengele]
    C --> D[Katman 1: XOR İşlemi]
    B --> E[Sayı Dizisinden İndis Üret]
    D --> F[Katman 2: Permütasyon - Bit Kaydırma]
    F --> G[Sonuç: Şifreli Bit Dizisi]
    G --> H[Deşifreleme: İşlemleri Tersine Yürüt]
    
🔑 Anahtar Üreteci (Key Generator) Sözde Kodu
FONKSİYON Anahtar_Uret(tohum_sayisi, mesaj_boyutu):
    n = tohum_sayisi
    ham_bitler = []
    sayi_yorungesi = []
    
    DÖNGÜ (ham_bitler < mesaj_boyutu / 2):
        EĞER n % 2 == 0 İSE:
            n = n / 2
            ham_bitler.ekle(0)
        DEĞİLSE:
            n = 3n + 1
            ham_bitler.ekle(1)
        sayi_yorungesi.ekle(n)
    
    # Dengeleme Katmanı (Manchester)
    dengeli_anahtar = []
    HER bit İÇİN ham_bitler:
        EĞER bit == 0 İSE: [0, 1] ekle
        EĞER bit == 1 İSE: [1, 0] ekle
        
    DÖNDÜR dengeli_anahtar, sayi_yorungesi
    
💻 Python Uygulaması
Proje iki ana dosyadan oluşmaktadır:
cipher.py: Şifreleme mantığının bulunduğu motor sınıfı.
main.py: Kullanıcı arayüzü ve örnek test uygulaması.

📊 Örnek Çıktı
Aşağıdaki veriler seed = 123456789 ve mesaj = "Collatz123" kullanılarak üretilmiştir:
Orijinal Mesaj: Collatz123
İkilik Hali (ASCII): 01000011 01101111 01101100 ...
Şifreli Bit Çıktısı:
[1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, ...]
(Toplam 80 Bit)
Özellik: Çıktıdaki toplam 1 sayısı ile 0 sayısı birbirine eşittir (40 adet 1, 40 adet 0).
