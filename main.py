import time
from modules.util import load_data, save_data, konversi_uang
from modules.auth import login, register_account
from modules.transaction import display_items, beli_barang

def top_up_gold(data, username):
    print("\n===== Top-Up Gold =====")
    try:
        rupiah = int(input("Masukkan jumlah Rupiah untuk top-up: "))
        if rupiah > 0:
            gold, sisa_rupiah = konversi_uang(rupiah)
            data["accounts"][username]["balance"]["Gold"] += gold
            print(f"Top-up berhasil! Anda mendapatkan {gold} Gold.")
            print(f"Sisa Rupiah (tidak terkonversi): {sisa_rupiah} Rupiah.\n")
            save_data(data)
        else:
            print("Jumlah harus lebih dari 0.")
    except ValueError:
        print("Input tidak valid. Masukkan angka yang benar.")

def main():
    data = load_data()

    while True:
        print("===== Selamat Datang di Ayam Geprek Em Said(Asli) =====")
        print("1. Login")
        print("2. Registrasi Akun")
        print("3. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            role, username = login(data["accounts"])
            if role:
                while True:
                    current_hour = time.localtime().tm_hour
                    if 5 <= current_hour < 12:
                        time_period = "pagi"
                    elif 12 <= current_hour < 18:
                        time_period = "siang"
                    else:
                        time_period = "malam"
                    
                    print(f"\n===== Menu Ayam Geprek - {time_period.upper()} =====")
                    print("1. Lihat Barang")
                    print("2. Beli Barang")
                    print("3. Top-Up Gold")
                    print("4. Logout")
                    user_input = input("Pilih menu: ")

                    if user_input == "1":
                        display_items(data["items"], time_period)
                    elif user_input == "2":
                        beli_barang(data["items"], data["voucher"], time_period, data, username)
                    elif user_input == "3":
                        top_up_gold(data, username)
                    elif user_input == "4":
                        print("Logout berhasil!")
                        break
                    else:
                        print("Menu tidak valid.")
        elif pilihan == "2":
            register_account(data)
        elif pilihan == "3":
            print("Terima kasih telah menggunakan layanan kami!")
            break
        else:
            print("Menu tidak valid.")

if __name__ == "__main__":
    main()
