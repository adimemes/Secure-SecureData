import pandas as pd
import random
import os

# Pastikan folder data/raw ada
os.makedirs('../data/raw', exist_ok=True)

# Template kalimat dengan placeholder
templates = [
    "Min, saldo gopay saya kok blm masuk?? pdhl udh transfer dr jam 7 pagi. Tolong cek no hp saya {phone}",
    "Aplikasi error trus nih, kecewa bgt. Balikin duit gue! Email gw {email}",
    "Hati2 guys penipuan, kmrn saya di tlp no {phone} ngaku dr CS, jgn pcaya.",
    "Tolong hapus akun saya dengan nik {nik}, saya mau ganti nomor baru.",
    "Admin tlg respon dm, sy udh kirim bukti trf ke email {email}. Thx.",
    "Gmn sih {app_name}?? topup via mbanking gagal mulu tp saldo kepotong. Balikin woy!",
    "Bagus bgt aplikasinya, tp verifikasi ktp lama bgt. No tiket keluhan sy {ticket}.",
    "Woi balikin duit gw 500rb!! jgn diem aja min.",
    "Topup {amount} jam segini lancar jaya, mantap min.",
    "Sy lupa pin, tlg reset ke email {email} atau wa ke {phone}. Urgent!!"
]

phones = ["081234567890", "0857-1122-3344", "+62818000999", "0813 4455 6677"]
emails = ["budi_geming@gmail.com", "siti.cantik123@yahoo.com", "user.disappointed@outlook.com", "admin.fake@hack.id"]
niks = ["3171234567890001", "3201123456780005"]
apps = ["GoPay", "OVO", "Dana", "Mobile Banking"]

data = []

# Generate 50 data dummy
for _ in range(50):
    temp = random.choice(templates)
    
    # Isi placeholder dengan data random
    text = temp.format(
        phone=random.choice(phones),
        email=random.choice(emails),
        nik=random.choice(niks),
        app_name=random.choice(apps),
        ticket=random.randint(10000, 99999),
        amount=f"Rp {random.randint(10, 100)}.000"
    )
    
    # Tambahkan variasi lowercase/uppercase biar makin 'kotor'
    if random.random() > 0.5:
        text = text.lower()
        
    data.append([text])

# Simpan ke CSV
df = pd.DataFrame(data, columns=['raw_text'])
df.to_csv('./data/raw/Data_Kotor.csv', index=False)

print("✅ Data berhasil dibuat di folder data/raw/Data_Kotor.csv")
print("Contoh data:")
print(df.head())