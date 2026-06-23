# 📦 Dashboard Simulasi Sistem Inventaris Gudang Retail (Siklus Berkelanjutan)

## 📝 Deskripsi Proyek
Proyek ini merupakan aplikasi simulator sistem manajemen inventaris operasional pergudangan berbasis Web (*Web Architecture*) yang dibangun menggunakan **Python** dan framework **Streamlit**. Simulasi ini memodelkan pergerakan stok barang harian dengan pendekatan kebijakan persediaan kuantitas pesanan tetap dan titik pemesanan kembali (**Fixed Order Quantity & Reorder Point System / Model Q**).

Tugas ini diselesaikan guna memenuhi kriteria kelulusan **Final Project Mata Kuliah Simulasi**. Mengingat kompleksitas menjadi indikator utama penilaian, proyek ini diimplementasikan menggunakan **Opsi 3 (Program Berbasis Python)** dengan arsitektur modular tingkat lanjut, visualisasi data interaktif, manajemen memori (*session state*), serta pengintegrasian simulasi stokastik pembangkit bilangan acak.

---

## 🚀 Fitur Utama & Kompleksitas Sistem
* **Arsitektur Modular (Separation of Concerns)**: Kode program secara fisik dipisah menjadi dua modul utama: `inventory_logic.py` (pemrosesan algoritma operasional murni) dan `app.py` (perancangan antarmuka pengguna).
* **Manajemen Siklus Berkelanjutan (State Management)**: Menggunakan `st.session_state` untuk menyimpan nilai penyimpanan terakhir (**Last Storage**) pada hari ke-50. Pengguna dapat melanjutkan simulasi ke siklus/bulan berikutnya secara kontinu tanpa mereset kondisi gudang.
* **Dual-Mode Pembangkitan Kebutuhan (Demand Generation)**:
  1. *Data Aktual (CSV)*: Menarik data riil historis dari file `50_hari_simulasi.csv`.
  2. *Simulasi Stokastik (Random Number)*: Membangkitkan bilangan acak secara otomatis berbasis **Distribusi Normal** menggunakan parameter statistik riil penjualan ritel (Mean = 136, Standard Deviasi = 40).
* **Data Caching (`@st.cache_data`)**: Mengoptimalkan performa runtime dengan menyimpan berkas CSV ke dalam memori RAM lokal sehingga proses pembacaan file tidak dieksekusi berulang kali saat pengguna mengubah parameter UI.
* **Dashboard Visual Interaktif (Plotly Engine)**: Visualisasi dinamika grafik garis persediaan yang responsif, dilengkapi *hover tooltip*, penandaan otomatis hari terjadinya kehabisan stok (*stockout*), serta kartu metrik evaluasi kinerja gudang.

---

## ⚙️ Persyaratan Sistem (Prerequisites)
Aplikasi ini berjalan pada ekosistem Python 3.x dan memerlukan pustaka eksternal berikut untuk direplikasi:
1. streamlit (Framework antarmuka Web UI)
2. pandas (Struktur data manipulasi tabel)
3. numpy (Komputasi numerik Distribusi Normal)
4. plotly (Mesin rendering grafik interaktif)

---

## 💻 Panduan Instalasi & Penggunaan
* **Metode 1: Pengoperasian Instan Satu Klik (Rekomendasi untuk Penguji)**
    Bagi pengguna yang ingin langsung meninjau hasil simulasi tanpa melalui command line, silakan ikuti langkah berikut:
*
1. Pastikan seluruh file berada dalam satu direktori folder yang utuh.
2. Lakukan klik ganda (double-click) pada file eksekusi Jalankan_Simulasi.bat.
3. Skrip akan otomatis memeriksa lingkungan kerja, mengunduh pustaka yang diperlukan, mengaktifkan server lokal,  dan meluncurkan dashboard pada web browser bawaan Anda.
* **Metode 2: Eksekusi Manual Melalui Terminal/CMD**
    Bagi pengembang yang ingin menjalankan sistem secara manual:
*
1. Buka Command Prompt / Terminal, lalu arahkan ke folder repositori proyek.
2. Instal seluruh dependensi yang diwajibkan:
    - Bash
    - pip install -r requirements.txt
3. Inisialisasi server lokal Streamlit:
    - Bash
    - python -m streamlit run app.py

---    

## 📊 Metrik Evaluasi Kinerja Gudang
Melalui panel samping (sidebar), pengguna dapat menguji sensitivitas nilai Reorder Point (ROP) dan Order Quantity (Q). Dashboard akan merespons secara real-time dan menyajikan empat indikator kuantitatif utama:
1. **Last Storage:** Sisa persediaan unit terakhir di gudang pada penutupan siklus simulasi. Parameter penting untuk mencegah indikasi Overstock.
2. **Total Shortage:** Akumulasi kuantitas permintaan pelanggan yang gagal terpenuhi akibat kekosongan stok. Target optimasi adalah menekan angka ini hingga mencapai 0.
3. **Hari Kehabisan Stok (Stockout):** Durasi kumulatif hari operasional di mana tingkat persediaan menyentuh titik nol.
4. **Frekuensi Order:** Jumlah total aktivitas pengadaan barang kembali (restock) kepada pihak supplier yang dipicu selama durasi simulasi berlangsung.

## Proyek Akhir Kelompok - Dikembangkan untuk Pemodelan Sistem Rantai Pasok dan Industri yang Efisien.



