import pandas as pd
import re
import os

# --- KONFIGURASI ---
INPUT_FILE = './data/raw/Data_Kotor.csv'
OUTPUT_FILE = './data/processed/Data_Bersih.csv'

# Kamus Normalisasi (Bisa ditambah nanti)
slang_dict = {
    "yg": "yang", "gk": "tidak", "ga": "tidak", "gak": "tidak",
    "sy": "saya", "gw": "saya", "aku": "saya", "gue": "saya",
    "blm": "belum", "udh": "sudah", "sdh": "sudah",
    "trf": "transfer", "tf": "transfer",
    "tlg": "tolong", "pls": "tolong",
    "dgn": "dengan", "dr": "dari",
    "bgt": "banget", "min": "admin",
    "balikin": "kembalikan", "woy": "",
    "tp": "tapi", "krn": "karena", "jd": "jadi"
}

def redact_pii(text):
    """
    Fungsi 'Killer Feature': Mendeteksi data pribadi dan menyensornya.
    Menggunakan Regular Expression (RegEx) yang disesuaikan untuk format Indonesia.
    """
    
    # 1. Redaksi Email
    # Pola: karakter apa saja + @ + domain
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    text = re.sub(email_pattern, '[EMAIL_SENSOR]', text)
    
    # 2. Redaksi Nomor HP Indonesia
    # Pola: Mulai dengan 08, 62, atau +62. Diikuti angka, spasi, atau strip. Panjang 9-14 karakter.
    phone_pattern = r'(\+62|62|08)[0-9\-\s]{9,15}'
    text = re.sub(phone_pattern, '[HP_SENSOR]', text)
    
    # 3. Redaksi NIK (16 digit angka)
    nik_pattern = r'\b\d{16}\b'
    text = re.sub(nik_pattern, '[NIK_SENSOR]', text)
    
    return text

def normalize_slang(text):
    """Mengubah kata alay menjadi baku berdasarkan kamus"""
    words = text.split()
    normalized_words = [slang_dict.get(word, word) for word in words]
    return " ".join(normalized_words)

def clean_text(text):
    """Pipeline utama pembersihan"""
    if not isinstance(text, str):
        return ""
    
    # 1. Lowercase dulu biar mudah dicocokkan
    text = text.lower()
    
    # 2. Jalankan PII Redaction (Sangat Penting!)
    text = redact_pii(text)
    
    # 3. Hapus karakter non-alphanumeric (kecuali spasi dan tag sensor kita)
    # Kita izinkan kurung siku [] dan underscore _ agar tag sensor tidak hilang
    text = re.sub(r'[^a-zA-Z0-9\s\[\]_]', '', text)
    
    # 4. Normalisasi Bahasa Alay
    text = normalize_slang(text)
    
    # 5. Hapus spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# --- EKSEKUSI UTAMA ---
if __name__ == "__main__":
    print("🚀 Memulai proses pembersihan data...")
    
    # Cek folder output
    os.makedirs('./data/processed', exist_ok=True)
    
    # Load Data
    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"✅ Data dimuat: {len(df)} baris")
        
        # Proses Cleaning
        # Kita buat kolom baru biar bisa compare Before vs After
        df['clean_text'] = df['raw_text'].apply(clean_text)
        
        # Simpan
        df.to_csv(OUTPUT_FILE, index=False)
        
        print("\n✨ CONTOH HASIL (Before vs After):")
        for i in range(5):
            print(f"Asli   : {df['raw_text'].iloc[i]}")
            print(f"Bersih : {df['clean_text'].iloc[i]}")
            print("-" * 50)
            
        print(f"\n✅ Data bersih tersimpan di: {OUTPUT_FILE}")
        
    except FileNotFoundError:
        print("❌ Error: File raw data tidak ditemukan. Jalankan generator.py dulu!")