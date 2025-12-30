from cipher import CollatzCipher


def main():
    # Arkadaşlarının bulması gereken gizli anahtar
    seed_value = 123456789
    cipher = CollatzCipher(seed_value)

    mesaj = "Collatz123"

    # Şifreleme
    sifreli_bitler = cipher.encrypt(mesaj)

    print("--- ŞİFRELEME BAŞARILI ---")
    print(f"Orijinal Mesaj: {mesaj}")
    print(f"Şifreli Çıktı (Bit Dizisi): {sifreli_bitler}")

    # Deşifreleme (Sadece bit dizisini kullanarak)
    cozulen_mesaj = cipher.decrypt(sifreli_bitler)
    print(f"\n--- DEŞİFRELEME SONUCU ---")
    print(f"Çözülen: {cozulen_mesaj}")


if __name__ == "__main__":
    main()