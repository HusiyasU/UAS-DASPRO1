import json
import os

def load_data(filepath="data/database.json"):
    if not os.path.exists("data"):
        os.makedirs("data")
        
    try:
        with open(filepath, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("File database.json tidak ditemukan. Membuat data baru.")
        data = {
            "accounts": {},
            "voucher": {
                "kode": "GEPREKDISKON",
                "diskon": 20,
                "used": False,
                "expired": False
            },
            "items": {
                "pagi": {"Nasi Ayam Geprek": 50, "Ayam Geprek Keju": 75},
                "siang": {"Ayam Geprek Sambal Matah": 60, "Paket Geprek Hemat": 100},
                "malam": {"Ayam Geprek Mozarella": 120, "Ayam Geprek Level 5": 80}
            }
        }
        save_data(data, filepath)
    return data

def save_data(data, filepath="data/database.json"):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

def konversi_uang(rp):
    gold = rp // 1000  # 1 Gold = 1000 Rupiah
    sisa_rp = rp % 1000
    return gold, sisa_rp
