import streamlit as st
import pandas as pd
import re

# --- LOGIKA LOAD DATA (Dictionary dari File) ---
def load_slang_dict():
    slang_dict = {}
    file_path = './data/slangword/combined_slang_words.txt'
    
    # 2. Baca file baris per baris
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Skip baris kosong atau yang berisi header 
                if not line or line.startswith("[source") or ":" not in line:
                    continue
                
                # Pisahkan kata gaul dan arti berdasarkan titik dua ':' pertama
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip().lower()   # Kata Gaul
                    value = parts[1].strip().lower() # Kata Asli
                    slang_dict[key] = value
                    
    except FileNotFoundError:
        st.error(f"⚠️ File kamus tidak ditemukan di: {file_path}")
        return {}
        
    return slang_dict

# --- LOGIKA CLEANING ---
def redact_pii(text):
    if not isinstance(text, str): return ""
    # Pola Email
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '📧[EMAIL_SENSOR]', text)
    # Pola No HP (+62, 62, 08)
    text = re.sub(r'(\+62|62|08)[0-9\-\s]{8,15}', '📱[HP_SENSOR]', text)
    # Pola NIK (16 digit angka)
    text = re.sub(r'\b\d{16}\b', '🆔[NIK_SENSOR]', text)
    return text

def normalize_slang(text):
    # Panggil fungsi load dictionary di sini
    slang_dict = load_slang_dict()
    
    words = text.split()
    # Cek setiap kata apakah ada di kamus
    normalized_words = [slang_dict.get(word, word) for word in words]
    return " ".join(normalized_words)

def clean_text_pipeline(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = redact_pii(text)
    # Hapus karakter aneh, sisakan huruf, angka, spasi, dan sensor tag
    text = re.sub(r'[^a-zA-Z0-9\s\[\]_📧📱🆔]', '', text) 
    text = normalize_slang(text)
    return re.sub(r'\s+', ' ', text).strip()

# --- TAMPILAN STREAMLIT ---
st.set_page_config(page_title="SecureData Pipeline", page_icon="🛡️")

st.title("🛡️ SecureData: PII Redaction & Cleaning")
st.markdown("Aplikasi ini menggunakan kamus slang dari file eksternal `.data/slangword`.")

# Tab Navigasi
tab1, tab2 = st.tabs(["⚡ Live Tester", "📂 Batch Processing (CSV)"])

# --- TAB 1: TEST MANUAL ---
with tab1:
    st.subheader("Uji Coba Teks")
    # Contoh teks default yang sesuai dengan kamus kamu (kmrn, tlp, jgn)
    user_input = st.text_area("")
    
    if st.button("Proses Teks"):
        with st.spinner('Membaca kamus slang & membersihkan data...'):
            result = clean_text_pipeline(user_input)
            
        col1, col2 = st.columns(2)
        with col1:
            st.info("**Original Input:**")
            st.write(user_input)
        with col2:
            st.success("**Cleaned Output:**")
            st.write(result)

# --- TAB 2: UPLOAD CSV ---
with tab2:
    st.subheader("Upload Dataset CSV")
    uploaded_file = st.file_uploader("Upload file CSV (pastikan ada kolom 'raw_text')", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Preview Data Asli:", df.head())
        
        if st.button("Proses Semua Data"):
            progress_bar = st.progress(0)
            df['clean_text'] = df['raw_text'].apply(clean_text_pipeline)
            progress_bar.progress(100)
            
            st.write("Preview Hasil:", df[['raw_text', 'clean_text']].head())
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Data Bersih",
                data=csv,
                file_name='secure_data_cleaned.csv',
                mime='text/csv',
            )