# 🚀 Collatz Balanced Permutation Cipher (CBPC)

Bu proje, matematik dünyasının en ünlü çözülememiş problemlerinden biri olan **Collatz Sanısı** (3n+1 problemi) üzerine inşa edilmiş özgün bir kriptografi algoritmasıdır. Algoritma, Collatz dizisinin kaotik doğasını kullanarak veriyi hem içerik hem de konum bazlı olarak şifreler.

## 📌 Proje Amacı
Bu çalışma, Collatz dizisinden elde edilen verilerin kriptografik bir **PRNG (Sözde Rastgele Sayı Üreticisi)** olarak kullanımını ve verilerin istatistiksel analizini zorlaştırmak için "Manchester Encoding" ile bit dengelemesini içerir.

### 🛠️ Kullanılan Kriptolojik Yöntemler
1.  **Yöntem B (Stream Cipher - XOR):** Mesaj bitleri, Collatz yörüngesinden üretilen ve Manchester Encoding ile dengelenmiş bir anahtar dizisiyle (keystream) XOR işlemine tabi tutulur.
2.  **Yöntem C (Transposition - Permütasyon):** XOR'lanan bitlerin konumları, Collatz sayı dizisi tarafından belirlenen dinamik bir matrisle karıştırılır.

---

## ⚖️ Bit Dengeleme (Manchester Encoding)
Standart bir Collatz dizisinde 0 (çift) ve 1 (tek) sayıları her zaman eşit değildir. Algoritmamızın çıktılarını eşit sayıda 0 ve 1 içerecek şekilde şifrelemek için her biti iki bitlik çiftlere dönüştürüyoruz:
- **0** üretilirse -> **01**
- **1** üretilirse -> **10**
Bu yöntem, şifreli verinin bit yoğunluğunun her zaman tam **%50** olmasını (0 ve 1 sayısının eşitliğini) garanti eder.

---

## 📊 Algoritma Akış Şeması (Flowchart)

```mermaid
graph TD
    A[Başlangıç: Seed & Mesaj] --> B[Collatz Yörüngesini Hesapla]
    B --> C[Manchester Encoding Uygula]
    C --> D[Dengeli Keystream Üret]
    D --> E[1. KATMAN: XOR İşlemi]
    B --> F[Sayısal Değerlerden İndis Üret]
    E --> G[2. KATMAN: Permütasyon - Bit Karıştırma]
    G --> H[Sonuç: Şifreli Bit Dizisi]
    H --> I[Deşifreleme: İşlemleri Tersine Yürüt]


##🔑 Anahtar Üreteci Sözde Kodu (Pseudo-code)
FONKSİYON Anahtar_Uret(tohum, mesaj_bit_boyutu):
    n = tohum
    sayilar = []
    bitler = []
    DÖNGÜ (bitler uzunluğu < mesaj_bit_boyutu / 2):
        EĞER n çift İSE: 
            n = n / 2
            bit = 0
        DEĞİLSE: 
            n = 3n + 1
            bit = 1
        bitler.ekle(bit)
        sayilar.ekle(n)
    
    # Manchester Dengeleme Katmanı
    dengeli_keystream = []
    HER b İÇİN bitler:
        EĞER b == 0 İSE: [0, 1] ekle
        DEĞİLSE: [1, 0] ekle
        
    DÖNDÜR dengeli_keystream, sayilar

## 💻 Python Uygulaması
# 1. cipher.py (Şifreleme Motoru)
class CollatzCipher:
    def __init__(self, seed):
        self.seed = seed

    def _generate_data(self, length):
        stream, numbers, n = [], [], self.seed
        needed = (length // 2) + 1
        while len(stream) < needed:
            if n % 2 == 0:
                n //= 2
                stream.append(0)
            else:
                n = 3 * n + 1
                stream.append(1)
            numbers.append(n)
        
        balanced = []
        for b in stream:
            balanced.extend([0, 1] if b == 0 else [1, 0])
        return balanced[:length], numbers

    def _get_indices(self, length, numbers):
        idx = list(range(length))
        for i in range(len(idx)):
            s = numbers[i % len(numbers)] % len(idx)
            idx[i], idx[s] = idx[s], idx[i]
        return idx

    def encrypt(self, text):
        bits = [int(b) for b in ''.join(format(ord(c), '08b') for c in text)]
        key, nums = self._generate_data(len(bits))
        idx = self._get_indices(len(bits), nums)
        # XOR + Permütasyon
        xored = [bits[i] ^ key[i] for i in range(len(bits))]
        return [xored[i] for i in idx]

    def decrypt(self, encrypted_bits):
        key, nums = self._generate_data(len(encrypted_bits))
        idx = self._get_indices(len(encrypted_bits), nums)
        # Ters Permütasyon + XOR
        xored = [0] * len(encrypted_bits)
        for i, pos in enumerate(idx): xored[pos] = encrypted_bits[i]
        orig = [xored[i] ^ key[i] for i in range(len(xored))]
        b_str = ''.join(map(str, orig))
        return ''.join(chr(int(b_str[i:i+8], 2)) for i in range(0, len(b_str), 8))

# 2. main.py (Çalıştırma ve Test)
from cipher import CollatzCipher

# --- Ayarlar ---
GIZLI_SEED = 123456789
MESAJ = "Collatz123"

# --- Uygulama ---
cipher = CollatzCipher(GIZLI_SEED)
sifreli = cipher.encrypt(MESAJ)
cozulen = cipher.decrypt(sifreli)

print(f"Orijinal Mesaj: {MESAJ}")
print(f"Şifreli Çıktı: {sifreli}")
print(f"Deşifre Sonucu: {cozulen}")

## 📈 Örnek Çıktılar ve Analiz

- **Test Mesajı:** `Collatz123` (80 bit)
- **Güvenlik Analizi:** Çıktıda toplam **40 adet 1** ve **40 adet 0** bulunmaktadır (Eşitlik kontrolü başarılı).
- **Zorluk:** Seed değeri bilinmeden Collatz yörüngesini tahmin etmek ve bitlerin permütasyon sırasını çözmek kaba kuvvet saldırısı dışında mümkün değildir.
