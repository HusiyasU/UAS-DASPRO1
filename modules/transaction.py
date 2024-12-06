from prettytable import PrettyTable
from modules.util import save_data, konversi_uang

def display_items(items, time_period):
    table = PrettyTable()
    table.field_names = ["No", "Nama Barang", "Harga (Gold)"]
    if time_period not in items:
        print("Tidak ada barang untuk periode waktu ini.")
        return []

    item_terdaftar = list(items[time_period].items())
    for index, (name, price) in enumerate(item_terdaftar, start=1):
        table.add_row([index, name, price])
    print(table)
    return item_terdaftar

def beli_barang(items, voucher, time_period, data, username):
    indexed_items = display_items(items, time_period)
    if not indexed_items:
        return

    try:
        pilihan = int(input("Masukkan nomor menu yang ingin dibeli: "))
        if 1 <= pilihan <= len(indexed_items):
            nama_barang, harga = indexed_items[pilihan - 1]
            print(f"Anda memilih: {nama_barang} dengan harga {harga} Gold.")

            user_balance = data["accounts"][username]["balance"]

            while user_balance["Gold"] < harga:
                print(f"Saldo Gold Anda ({user_balance['Gold']} Gold) tidak mencukupi.")
                pilihan_topup = input("Apakah Anda ingin melakukan top-up? (ya/tidak): ").strip().lower()
                if pilihan_topup == "ya":
                    try:
                        rupiah = int(input("Masukkan jumlah Uang (Rp) untuk top-up: "))
                        if rupiah > 0:
                            gold, _ = konversi_uang(rupiah)
                            user_balance["Gold"] += gold
                            save_data(data)
                            print(f"Saldo Gold Anda sekarang: {user_balance['Gold']} Gold.")
                        else:
                            print("Top-up gagal. Jumlah Uang harus lebih dari 0.")
                    except ValueError:
                        print("Input tidak valid. Masukkan jumlah uang yang benar.")
                else:
                    print("Transaksi dibatalkan.")
                    return

            gunakan_voucher = input("Apakah Anda ingin menggunakan voucher? (ya/tidak): ").strip().lower()
            if gunakan_voucher == "ya" and not data["voucher"]["used"] and not data["voucher"]["expired"]:
                harga -= data["voucher"]["diskon"]
                data["voucher"]["used"] = True
                print(f"Voucher digunakan! Diskon {data['voucher']['diskon']} Gold. Harga akhir: {harga} Gold.")
            elif data["voucher"]["used"]:
                print("Voucher sudah digunakan.")
            elif data["voucher"]["expired"]:
                print("Voucher sudah kedaluwarsa.")

            user_balance["Gold"] -= harga
            print(f"Pembelian berhasil! Sisa Gold Anda: {user_balance['Gold']} Gold.")
            save_data(data)
        else:
            print("Nomor menu tidak valid.")
    except ValueError:
        print("Input harus berupa angka.")
