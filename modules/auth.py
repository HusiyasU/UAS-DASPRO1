import pwinput
from modules.util import save_data
import re

def register_account(data):
    print("\n==== Daftar Akun Cik ====")
    
    username = input("Masukkan username: ").strip()
    if username in data["accounts"]:
        print("Username sudah terdaftar. Silakan gunakan username lain.")
        return

    while True:
        password = pwinput.pwinput("Masukkan password: ").strip()
        if len(password) >= 6 and re.search("[A-Za-z]", password) and re.search("[0-9]", password):
            break
        print("Password harus minimal 6 karakter, mengandung huruf dan angka.")

    while True:
        role = input("Pilih role akun (Biasa/VIP): ").strip().lower()
        if role in ["biasa", "vip"]:
            break
        print("Role tidak valid. Pilih antara 'Biasa' atau 'VIP'.")

    data["accounts"][username] = {
        "password": password,
        "role": role,
        "locked": False,
        "attempts": 0,
        "balance": {"Gold": 0}
    }
    save_data(data)  
    print(f"Akun dengan username '{username}' berhasil dibuat!\n")

def login(accounts):
    print("=== Login Akun ===")
    for attempt in range(3):
        username = input("Masukkan username: ").strip()
        password = pwinput.pwinput("Masukkan password: ").strip()

        if username in accounts:
            account = accounts[username]

            if account["locked"]:
                print("Akun Anda terkunci. Silakan hubungi admin.")
                return None, None

            if account["password"] == password:
                print(f"Login berhasil! Selamat datang, {username}.")
                account["attempts"] = 0  # Reset attempts
                return account["role"], username
            else:
                print("Password salah.")
                account["attempts"] += 1

                if account["attempts"] >= 3:
                    account["locked"] = True
                    print("Akun terkunci karena terlalu banyak percobaan salah.")
        else:
            print("Username tidak ditemukan.")
    return None, None
