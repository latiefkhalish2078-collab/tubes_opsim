# 📦 Dashboard Simulasi Inventory Retail (50 Hari)

## Deskripsi Proyek
Proyek ini adalah simulasi sistem inventaris (pergudangan) berbasis web yang dibangun menggunakan Python dan Streamlit. Program ini menyimulasikan pergerakan stok harian selama 50 hari ke depan berdasarkan data historis permintaan (demand). 
Tujuan utamanya adalah mencari titik keseimbangan antara mencegah kehabisan barang (*stockout*) dan menghindari penumpukan barang (*overstock*).

## Fitur Utama
* **Input Dinamis**: Pengguna dapat mengubah *Inventory Awal, Reorder Point (ROP), Order Quantity,* dan *Lead Time* secara interaktif.
* **Integrasi Data Aktual**: Menggunakan data historis `50_hari_simulasi.csv` sebagai dasar permintaan (demand) harian.
* **Kalkulasi Otomatis**: Menghitung secara rinci jadwal kedatangan barang, stok pagi, stok sore, dan jumlah *shortage* setiap hari.
* **Visualisasi Real-time**: Menyediakan grafik garis interaktif yang langsung diperbarui setiap kali parameter diubah.
* **Metrik Evaluasi**: Menampilkan ringkasan total shortage, frekuensi pemesanan, jumlah hari stockout, dan rata-rata stok harian.

## Persyaratan Sistem (Prerequisites)
Pastikan Python 3.x sudah terinstal di sistem Anda beserta *library* berikut:
* `streamlit`
* `pandas`
* `matplotlib`

*(Install dependensi dengan menjalankan: `pip install streamlit pandas matplotlib`)*

## Struktur File
1. `app.py` : Berisi kode sumber utama untuk logika simulasi dan antarmuka Streamlit.
2. `50_hari_simulasi.csv` : Dataset yang berisi angka permintaan (demand) riil selama 50 hari (kolom 'Units Sold').
3. `Aplikasi Simulasi Inventory.bat` : *Executable shortcut* untuk Windows agar program bisa dijalankan dengan satu kali klik.

## Cara Menjalankan Program
**Untuk Pengguna Windows:**
Cukup klik dua kali (double-click) pada file `Aplikasi Simulasi Inventory.bat`. Browser akan otomatis terbuka dan menampilkan dashboard.

**Cara Manual (Terminal/CMD):**
1. Buka Terminal / Command Prompt.
2. Arahkan ke direktori folder penyimpan file.
3. Jalankan perintah berikut: `python -m streamlit run app.py`

---
