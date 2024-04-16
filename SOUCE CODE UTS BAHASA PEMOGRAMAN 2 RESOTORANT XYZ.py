import sqlite3

class Menu:
    def __init__(self):
        self.conn = sqlite3.connect('restoran.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS menu
                         (nama TEXT PRIMARY KEY,
                          harga INTEGER,
                          stok INTEGER)''')
        self.conn.commit()

    def tambah_makanan(self, nama, harga, stok):
        try:
            self.c.execute("INSERT INTO menu (nama, harga, stok) VALUES (?, ?, ?)", (nama, harga, stok))
            self.conn.commit()
            print(f"Makanan '{nama}' berhasil ditambahkan ke menu.")
        except sqlite3.IntegrityError:
            print(f"Makanan '{nama}' sudah ada di menu.")

    def tampilkan_menu(self):
        self.c.execute("SELECT * FROM menu")
        rows = self.c.fetchall()
        if rows:
            print("=== MENU MAKANAN ===")
            print("{:<20} {:<10} {:<10}".format("NAMA", "HARGA", "STOK"))
            print("-" * 40)
            for row in rows:
                print("{:<20} {:<10} {:<10}".format(row[0], f"Rp.{row[1]}", row[2]))
        else:
            print("Menu kosong.")

    def beli_makanan(self, pesanan):
        total_harga = 0
        for nama, jumlah in pesanan.items():
            self.c.execute("SELECT harga, stok FROM menu WHERE nama=?", (nama,))
            row = self.c.fetchone()
            if row:
                harga = row[0]
                stok = row[1]
                if stok >= jumlah:
                    total_harga += harga * jumlah
                else:
                    print(f"Maaf, stok {nama} tidak mencukupi.")
                    return 0
            else:
                print(f"{nama} tidak tersedia.")
                return 0
        return total_harga

    def kurangi_stok(self, pesanan):
        for nama, jumlah in pesanan.items():
            self.c.execute("UPDATE menu SET stok = stok - ? WHERE nama = ?", (jumlah, nama))
            self.conn.commit()

    def perbarui_menu(self, nama, harga_baru, stok_baru):
        self.c.execute("UPDATE menu SET harga = ?, stok = ? WHERE nama = ?", (harga_baru, stok_baru, nama))
        self.conn.commit()
        print(f"Menu '{nama}' berhasil diperbarui.")

def cetak_struk(pesanan, total_harga, pembayaran, kembalian):
    print("\n=== STRUK PEMBELIAN ===")
    print("{:<20} {:<10}".format("NAMA", "JUMLAH"))
    print("-" * 30)
    for nama, jumlah in pesanan.items():
        print("{:<20} {:<10}".format(nama, jumlah))
    print(f"Total harga : Rp.{total_harga}")
    print(f"Pembayaran  : Rp.{pembayaran}")
    print(f"Kembalian   : Rp.{kembalian}")
    print("=======================")

def pesan_makanan(menu):
    pesanan = {}
    while True:
        nama_makanan = input("Masukkan nama makanan yang ingin dipesan (ketik 'selesai' untuk selesai): ")
        if nama_makanan.lower() == 'selesai':
            break
        jumlah_pesanan = int(input("Masukkan jumlah: "))
        pesanan[nama_makanan] = jumlah_pesanan
    return pesanan

def main():
    restoran_menu = Menu()

    while True:
        print("\n=== RESTORAN XYZ ===")
        print("1. Tampilkan Menu")
        print("2. Beli Makanan")
        print("3. Tambah Menu")
        print("4. Perbarui Menu")
        print("5. Keluar")

        choice = input("Pilih menu: ")

        if choice == '1':
            restoran_menu.tampilkan_menu()

        elif choice == '2':
            pesanan = pesan_makanan(restoran_menu)
            total_harga = restoran_menu.beli_makanan(pesanan)
            if total_harga > 0:
                print(f"Total harga: Rp.{total_harga}")
                pembayaran = int(input("Masukkan nominal pembayaran: Rp."))
                kembalian = pembayaran - total_harga
                if kembalian >= 0:
                    print(f"Kembalian: Rp.{kembalian}")
                    restoran_menu.kurangi_stok(pesanan)
                    cetak_struk(pesanan, total_harga, pembayaran, kembalian)
                else:
                    print("Maaf, uang Anda tidak mencukupi.")

        elif choice == '3':
            nama = input("Nama Menu: ")
            harga = int(input("Harga: Rp."))
            stok = int(input("Stok: "))
            restoran_menu.tambah_makanan(nama, harga, stok)

        elif choice == '4':
            nama = input("Nama Menu yang akan diperbarui: ")
            harga_baru = int(input("Harga baru: Rp."))
            stok_baru = int(input("Stok baru: "))
            restoran_menu.perbarui_menu(nama, harga_baru, stok_baru)

        elif choice == '5':
            print("Terima kasih telah menggunakan layanan kami!")
            break

        else:
            print("Pilihan tidak valid. Silakan pilih menu yang benar.")

    restoran_menu.conn.close()

if __name__ == "__main__":
    main()
