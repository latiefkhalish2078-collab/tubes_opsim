import csv
import math
import random

def cetak_garis():
    print("+" + "-"*8 + "+" + "-"*15 + "+" + "-"*16 + "+" + "-"*19 + "+" + "-"*16 + "+" + "-"*12 + "+" + "-"*12 + "+")

def jalankan_simulasi(inv_awal, rop, qty_order, lead_time, hari_simulasi, mode_demand, demand_csv=None):
    jadwal_kedatangan = {}
    history_simulasi = []
    stok_awal_hari_ini = inv_awal
    
    total_shortage = 0
    hari_stockout = 0
    total_pesanan = 0
    total_stok_akhir = 0

    print("\n" + "="*50)
    print(f"       PROSES SIMULASI BERJALAN ({hari_simulasi} HARI)")
    print("="*50)
    cetak_garis()
    print(f"| {'Hari'.center(6)} | {'Barang Datang'.center(13)} | {'Inventory Pagi'.center(14)} | {'Demand (Permintaan)'.center(17)} | {'Inventory Sore'.center(14)} | {'Shortage'.center(10)} | {'Pesan?'.center(10)} |")
    cetak_garis()

    for hari in range(1, hari_simulasi + 1):
        # Cek barang datang pagi
        barang_datang = jadwal_kedatangan.get(hari, 0)
        stok_pagi = stok_awal_hari_ini + barang_datang
        
        # Penentuan Demand 
        if mode_demand == '1' and demand_csv and (hari - 1) < len(demand_csv):
            demand = demand_csv[hari - 1]
            catatan_demand = f"{demand} (CSV)"
        else:
            # Random Number
            demand = max(0, int(random.normalvariate(136, 40)))
            catatan_demand = f"{demand} (RND)"
            
        # Hitung stok sore dan shortage
        stok_sore = max(0, stok_pagi - demand)
        shortage = max(0, demand - stok_pagi)
        
        # Logika Pemesanan Barang (Mencegah Double Order)
        status_pesan = "Tidak"
        sedang_menunggu = any(k > hari for k in jadwal_kedatangan.keys())
        
        if stok_sore <= rop and not sedang_menunggu:
            status_pesan = "Ya"
            hari_datang = hari + lead_time + 1
            jadwal_kedatangan[hari_datang] = qty_order
            total_pesanan += 1

        # Rekap Statistik
        total_shortage += shortage
        if stok_sore == 0:
            hari_stockout += 1
        total_stok_akhir += stok_sore

        print(f"| {str(hari).center(6)} | {str(barang_datang).center(13)} | {str(stok_pagi).center(14)} | {catatan_demand.center(17)} | {str(stok_sore).center(14)} | {str(shortage).center(10)} | {status_pesan.center(10)} |")
        
        # Persiapan hari berikutnya
        stok_awal_hari_ini = stok_sore

    cetak_garis()
    
    # Last Storage
    last_storage = stok_sore
    rata_rata_stok = total_stok_akhir / hari_simulasi

    # Tampilan Analisis Performa
    print("\n" + "="*50)
    print("             HASIL EVALUASI SIMULASI            ")
    print("="*50)
    print(f"1. Total Unit Gagal Terpenuhi (Shortage) : {total_shortage} unit")
    print(f"2. Frekuensi Pemesanan Barang (Order)    : {total_pesanan} kali")
    print(f"3. Jumlah Hari Kehabisan Stok (Stockout) : {hari_stockout} hari")
    print(f"4. Rata-rata Stok Gudang Harian          : {rata_rata_stok:.2f} unit")
    print(f"5. PENYIMPANAN TERAKHIR (LAST STORAGE)   : {last_storage} unit")
    print("="*50)
    
    return last_storage

def main():
    print("="*50)
    print("    SISTEM SIMULASI OPERASIONAL INVENTORY RETAIL   ")
    print("="*50)

    # Membaca data CSV pendukung jika ada
    demand_csv = []
    try:
        with open('50_hari_simulasi.csv', mode='r') as file:
            reader = csv.reader(file)
            header = next(reader) # skip header
            # Cari index Units Sold
            idx = header.index('Units Sold') if 'Units Sold' in header else 5
            for row in reader:
                if row:
                    demand_csv.append(int(row[idx]))
        print("Berhasil memuat data historis dari '50_hari_simulasi.csv'")
    except (FileNotFoundError, ValueError, IndexError):
        print("Catatan: File '50_hari_simulasi.csv' tidak ditemukan/format berbeda.")
        print("   Simulasi akan dialihkan penuh menggunakan Generator Angka Acak.")

    # Pilihan Mode Pengolahan Angka Permintaan
    print("\nPilih Metode Pembangkitan Permintaan (Demand):")
    print("[1] Menggunakan Data Aktual CSV Historis")
    print("[2] Menggunakan Bilangan Acak (Random Number Generator)")
    mode_demand = input("Masukkan pilihan (1/2): ") or '2'

    # Input parameter operasional awal
    inv_awal = int(input("\nMasukkan Inventory Awal: ") or 500)
    rop = int(input("Masukkan Reorder Point (ROP): ") or 100)
    qty_order = int(input("Masukkan Kuantitas Pesanan (Q): ") or 200)
    lead_time = int(input("Masukkan Lead Time Pengiriman (Hari): ") or 2)
    hari_simulasi = int(input("Masukkan Durasi Hari Simulasi: ") or 50)

    # Simulasi siklus pertama
    last_storage = jalankan_simulasi(inv_awal, rop, qty_order, lead_time, hari_simulasi, mode_demand, demand_csv)

    # Logika Pengulangan Berkelanjutan
    while True:
        kontinu = input("\nApakah ingin melanjutkan simulasi ke siklus berikutnya? (y/n): ").lower()
        if kontinu == 'y':
            hari_lanjutan = int(input("Masukkan jumlah hari tambahan simulasi: ") or 30)
            print(f"\n>> Menjalankan simulasi lanjutan dengan Inventory Awal diambil dari LAST STORAGE sebelumnya: {last_storage} unit.")
            
            # Jalankan ulang dengan inv_awal = last_storage sebelumnya
            last_storage = jalankan_simulasi(last_storage, rop, qty_order, lead_time, hari_lanjutan, mode_demand, demand_csv)
        else:
            print("\nTerima kasih. Program simulasi selesai.")
            break

if __name__ == "__main__":
    main()


