import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi Halaman Web
st.set_page_config(page_title="Simulasi Inventory", layout="wide")
st.title("📦 Dashboard Simulasi Inventory Retail")
st.markdown("Proyek Akhir Simulasi Sistem Pergudangan menggunakan logika Reorder Point (ROP).")

# ==========================================
# SIDEBAR UNTUK INPUT VARIABEL
# ==========================================
st.sidebar.header("⚙️ Parameter Input")
inv_awal = st.sidebar.slider("Inventory Awal", min_value=100, max_value=1000, value=500, step=50)
rop = st.sidebar.slider("Reorder Point (ROP)", min_value=50, max_value=500, value=100, step=10)
qty_order = st.sidebar.slider("Order Quantity", min_value=50, max_value=1000, value=200, step=50)
lead_time = st.sidebar.slider("Lead Time (Hari)", min_value=1, max_value=7, value=2, step=1)

# ==========================================
# MEMUAT DATA DEMAND
# ==========================================
try:
    # 1. Baca data (default koma)
    df_data = pd.read_csv('50_hari_simulasi.csv')
    
    # 2. Cek apakah format CSV menggunakan titik koma (khas PC Indonesia)
    if len(df_data.columns) == 1:
        df_data = pd.read_csv('50_hari_simulasi.csv', sep=';')
        
    # 3. Bersihkan spasi tersembunyi di awal/akhir nama kolom
    df_data.columns = df_data.columns.str.strip()
    
    # 4. Ambil 50 data pertama
    demand_harian = df_data['Units Sold'].head(50).tolist()
    
except FileNotFoundError:
    st.error("File '50_hari_simulasi.csv' tidak ditemukan. Pastikan file berada di folder yang sama.")
    st.stop()
except KeyError:
    st.error("Kolom 'Units Sold' tetap tidak ditemukan! Berikut adalah daftar kolom yang terbaca oleh program:")
    st.write(df_data.columns.tolist())
    st.stop()

# ==========================================
# PROSES SIMULASI
# ==========================================
hari_simulasi = len(demand_harian)
jadwal_kedatangan = {} 
history_simulasi = []  
stok_awal_hari_ini = inv_awal

for hari in range(1, hari_simulasi + 1):
    barang_datang = jadwal_kedatangan.get(hari, 0)
    stok_pagi = stok_awal_hari_ini + barang_datang
    demand = demand_harian[hari - 1]
    
    stok_sore = max(0, stok_pagi - demand)
    shortage = max(0, demand - stok_pagi)
    
    status_pesan = "Tidak"
    sedang_menunggu = any(k > hari for k in jadwal_kedatangan.keys())
    
    if stok_sore <= rop and not sedang_menunggu:
        status_pesan = "Ya"
        hari_datang = hari + lead_time + 1
        jadwal_kedatangan[hari_datang] = qty_order
        
    history_simulasi.append({
        "Hari": hari,
        "Barang Datang": barang_datang,
        "Stok Pagi": stok_pagi,
        "Demand": demand,
        "Stok Akhir": stok_sore,
        "Shortage": shortage,
        "Pesan Barang?": status_pesan
    })
    
    stok_awal_hari_ini = stok_sore

df_hasil = pd.DataFrame(history_simulasi)

# ==========================================
# TAMPILAN METRIK (KARTU STATISTIK)
# ==========================================
total_shortage = df_hasil['Shortage'].sum()
hari_stockout = len(df_hasil[df_hasil['Stok Akhir'] == 0])
total_pesanan = len(df_hasil[df_hasil['Pesan Barang?'] == 'Ya'])
rata_rata_stok = df_hasil['Stok Akhir'].mean()

st.subheader("📊 Ringkasan Performa")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Shortage (Unit)", f"{total_shortage}")
col2.metric("Hari Stockout", f"{hari_stockout} Hari")
col3.metric("Frekuensi Pemesanan", f"{total_pesanan} Kali")
col4.metric("Rata-rata Stok Harian", f"{rata_rata_stok:.0f} Unit")

# ==========================================
# TAMPILAN GRAFIK
# ==========================================
st.subheader("📈 Visualisasi Pergerakan Stok")
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(df_hasil['Hari'], df_hasil['Stok Akhir'], marker='o', linestyle='-', color='#1f77b4', label='Stok Akhir')
ax.axhline(y=rop, color='red', linestyle='--', label=f'Batas ROP ({rop})')

# Menandai titik stockout dengan warna merah
stockout_points = df_hasil[df_hasil['Stok Akhir'] == 0]
ax.scatter(stockout_points['Hari'], stockout_points['Stok Akhir'], color='red', s=100, zorder=5, label='Stok Habis!')

ax.set_xlabel('Hari ke-')
ax.set_ylabel('Jumlah Unit')
ax.legend()
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# ==========================================
# TAMPILAN TABEL
# ==========================================
st.subheader("📋 Tabel Detail Simulasi")
st.dataframe(df_hasil, use_container_width=True)

