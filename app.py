# ============================================================
# CELL 3: MEMBUAT FILE APP.PY (DASHBOARD PENJUALAN)
# ============================================================

with open("app.py", "w") as f:
    f.write("""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="Dashboard Penjualan", page_icon="🛒", layout="wide")

st.title("🛒 Dashboard Penjualan")
st.caption("Visualisasi data penjualan interaktif — 500 records dari 7 produk & 7 kota")

@st.cache_data
def load_data():
    produk = ['Laptop', 'Smartphone', 'Tablet', 'Headphone', 'Speaker', 'Smartwatch', 'Camera']
    kota = ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Palembang', 'Makassar', 'Yogyakarta']
    start_date = datetime(2023, 1, 1)
    
    df = pd.DataFrame({
        'tanggal': [start_date + timedelta(days=np.random.randint(0, 730)) for _ in range(500)],
        'produk': np.random.choice(produk, 500),
        'kota': np.random.choice(kota, 500),
        'pendapatan': np.random.randint(500000, 5000000, 500),
        'unit_terjual': np.random.randint(1, 100, 500),
    })
    df['tanggal'] = pd.to_datetime(df['tanggal'])
    df = df.sort_values('tanggal').reset_index(drop=True)
    return df

df = load_data()

st.sidebar.header("🔍 Filter Data")

produk_list = df['produk'].unique().tolist()
produk_pilihan = st.sidebar.multiselect("Pilih Produk", options=produk_list, default=produk_list)

kota_list = df['kota'].unique().tolist()
kota_pilihan = st.sidebar.multiselect("Pilih Kota", options=kota_list, default=kota_list)

df_filtered = df[df['produk'].isin(produk_pilihan) & df['kota'].isin(kota_pilihan)]

col1, col2, col3 = st.columns(3)
total_pendapatan = df_filtered['pendapatan'].sum()
rata_pendapatan = df_filtered['pendapatan'].mean()
produk_terlaris = df_filtered.groupby('produk')['pendapatan'].sum().idxmax() if not df_filtered.empty else "-"

col1.metric("💰 Total Pendapatan", f"Rp {total_pendapatan:,.0f}")
col2.metric("📊 Rata-rata Pendapatan", f"Rp {rata_pendapatan:,.0f}")
col3.metric("🏆 Produk Terlaris", produk_terlaris)

st.subheader("📈 Tren Pendapatan Bulanan")
df_filtered['bulan'] = df_filtered['tanggal'].dt.to_period('M').dt.start_time
pendapatan_bulanan = df_filtered.groupby('bulan')['pendapatan'].sum().reset_index()
fig1 = px.line(pendapatan_bulanan, x='bulan', y='pendapatan', markers=True, color_discrete_sequence=['#E0654A'])
fig1.update_layout(template='plotly_white', hovermode='x unified')
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📊 Total Pendapatan per Produk")
pendapatan_produk = df_filtered.groupby('produk')['pendapatan'].sum().reset_index().sort_values('pendapatan', ascending=False)
fig2 = px.bar(pendapatan_produk, x='produk', y='pendapatan', color='produk', color_discrete_sequence=px.colors.sequential.Oranges_r, text='pendapatan')
fig2.update_traces(textposition='outside', texttemplate='%{text:,.0f}')
fig2.update_layout(template='plotly_white', showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("🗺️ Peta Pendapatan per Kota")
koordinat_kota = {
    'Jakarta': (-6.2088, 106.8456), 'Surabaya': (-7.2575, 112.7521),
    'Bandung': (-6.9175, 107.6191), 'Medan': (3.5952, 98.6722),
    'Palembang': (-2.9761, 104.7754), 'Makassar': (-5.1477, 119.4327),
    'Yogyakarta': (-7.7971, 110.3688)
}
pendapatan_kota = df_filtered.groupby('kota')['pendapatan'].sum().reset_index()
if not pendapatan_kota.empty:
    pendapatan_kota['lat'] = pendapatan_kota['kota'].map(lambda x: koordinat_kota[x][0])
    pendapatan_kota['lon'] = pendapatan_kota['kota'].map(lambda x: koordinat_kota[x][1])
    fig3 = px.scatter_mapbox(pendapatan_kota, lat='lat', lon='lon', size='pendapatan', color='pendapatan',
                              hover_name='kota', color_continuous_scale='OrRd', size_max=50,
                              zoom=3.5, center={'lat': -3, 'lon': 118})
    fig3.update_layout(mapbox_style='open-street-map')
    st.plotly_chart(fig3, use_container_width=True)

with st.expander("📋 Lihat Data Mentah"):
    st.dataframe(df_filtered)
""")

print("✅ File app.py berhasil dibuat!")