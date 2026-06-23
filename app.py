import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# DATA ACCESS 
@st.cache_data
def load_demand_data(filepath, hari_simulasi):
    """Membaca data CSV dan menyimpannya di Cache agar tidak dibaca berulang kali."""
    try:
        df_data = pd.read_csv(filepath)
        if len(df_data.columns) == 1:
            df_data = pd.read_csv(filepath, sep=';')
        df_data.columns = df_data.columns.str.strip()
        
        demand_raw = df_data['Units Sold'].tolist()
        # Sesuaikan panjang array dengan hari simulasi
        return demand_raw[:hari_simulasi] + [0] * max(0, hari_simulasi - len(demand_raw))
    except Exception:
        return None

def generate_random_demand(seed, hari_simulasi, mean=136, std=40):
    """Membangkitkan data demand acak berbasis Distribusi Normal."""
    np.random.seed(seed)
    demand_acak = np.random.normal(loc=mean, scale=std, size=hari_simulasi)
    return [max(0, int(x)) for x in demand_acak]

# LOGIC
def calculate_inventory_simulation(inv_awal, rop, qty_order, lead_time, demand_harian):
    """Memproses algoritma operasional gudang dan mengembalikan DataFrame."""
    jadwal_kedatangan = {}
    history_simulasi = []
    stok_awal_hari_ini = inv_awal
    hari_simulasi = len(demand_harian)

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
            "Inv Pagi": stok_pagi,
            "Demand": demand,
            "Inv Akhir": stok_sore,
            "Shortage": shortage,
            "Pesan": status_pesan
        })
        stok_awal_hari_ini = stok_sore

    return pd.DataFrame(history_simulasi)

# UI
def main():
    st.set_page_config(page_title="Retail Inventory Ops", layout="wide", page_icon="📦")

    # Inisialisasi Manajemen State
    if 'inv_awal' not in st.session_state:
        st.session_state.inv_awal = 500
    if 'siklus_ke' not in st.session_state:
        st.session_state.siklus_ke = 1

    st.title("Sistem Pemantauan & Simulasi Inventaris")
    st.markdown(f"**Siklus Simulasi Ke- {st.session_state.siklus_ke}**")
    st.divider()

    # UI: SIDEBAR 
    with st.sidebar:
        st.header("Konfigurasi Sistem")
        mode_demand = st.radio("Sumber Data:", ["Data Aktual (CSV)", "Random (Distribusi Normal)"])
        
        st.subheader("Parameter Gudang")
        inv_awal_input = st.number_input("Inventory Awal", value=st.session_state.inv_awal, step=50)
        st.session_state.inv_awal = inv_awal_input 
        
        rop = st.slider("Reorder Point (ROP)", 50, 500, 100, 10)
        qty_order = st.slider("Order Quantity (Q)", 50, 1000, 200, 50)
        lead_time = st.slider("Lead Time (Hari)", 1, 7, 2)
        hari_simulasi = st.number_input("Durasi Simulasi (Hari)", value=50, min_value=10)

    # PENGAMBILAN DATA
    if mode_demand == "Data Aktual (CSV)":
        demand_harian = load_demand_data('50_hari_simulasi.csv', hari_simulasi)
        if demand_harian is None:
            st.sidebar.error("CSV Gagal dimuat. Menggunakan Random.")
            demand_harian = generate_random_demand(st.session_state.siklus_ke, hari_simulasi)
    else:
        demand_harian = generate_random_demand(st.session_state.siklus_ke, hari_simulasi)

    # EKSEKUSI LOGIKA
    df_hasil = calculate_inventory_simulation(st.session_state.inv_awal, rop, qty_order, lead_time, demand_harian)
    last_storage = df_hasil.iloc[-1]["Inv Akhir"]

    # UI: VISUALISASI 
    tab1, tab2, tab3 = st.tabs(["Dashboard Visual", "Tabel Data Operasional", "Manajemen Siklus"])

    with tab1:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Last Storage", f"{last_storage} Unit")
        c2.metric("Total Shortage", f"{df_hasil['Shortage'].sum()} Unit")
        c3.metric("Hari Stockout", f"{len(df_hasil[df_hasil['Inv Akhir'] == 0])} Hari")
        c4.metric("Frekuensi Order", f"{len(df_hasil[df_hasil['Pesan'] == 'Ya'])} Kali")

        # Grafik Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_hasil['Hari'], y=df_hasil['Inv Akhir'], mode='lines+markers', name='Level Stok'))
        fig.add_trace(go.Scatter(x=[1, hari_simulasi], y=[rop, rop], mode='lines', name='Batas ROP', line=dict(color='red', dash='dash')))
        
        df_stockout = df_hasil[df_hasil['Inv Akhir'] == 0]
        if not df_stockout.empty:
            fig.add_trace(go.Scatter(x=df_stockout['Hari'], y=df_stockout['Inv Akhir'], mode='markers', name='Stok Habis', marker=dict(color='red', size=12, symbol='x')))
            
        fig.update_layout(title="Pergerakan Inventaris Harian", hovermode="x unified", height=400)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.dataframe(df_hasil, use_container_width=True)

    with tab3:
        st.write(f"Stok Akhir Saat Ini: **{last_storage} Unit**")
        if st.button("Lanjutkan ke Siklus Berikutnya", type="primary"):
            st.session_state.inv_awal = int(last_storage)
            st.session_state.siklus_ke += 1
            st.rerun()

# Eksekusi Utama
if __name__ == "__main__":
    main()


