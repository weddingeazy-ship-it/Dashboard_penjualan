import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="Dashboard Cuaca", page_icon="🌤️", layout="wide")
st.title("🌤️ Dashboard Cuaca Indonesia")

# Buat data (langsung di dalam kode, karena nggak ada file CSV)
start_date = datetime(2023, 1, 1)
cities = ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Palembang', 'Makassar', 'Yogyakarta']

df = pd.DataFrame({
    'tanggal': [start_date + timedelta(days=np.random.randint(0, 730)) for _ in range(500)],
    'kota': np.random.choice(cities, 500),
    'suhu': np.random.randint(22, 35, 500),
    'curah_hujan': np.random.randint(0, 300, 500),
    'kelembaban': np.random.randint(60, 95, 500),
})
df['tanggal'] = pd.to_datetime(df['tanggal'])
df = df.sort_values('tanggal').reset_index(drop=True)

# Sidebar filter
st.sidebar.header("🔍 Filter Kota")
kota_list = df['kota'].unique().tolist()
kota_pilihan = st.sidebar.multiselect("Pilih Kota", options=kota_list, default=kota_list)
df_filtered = df[df['kota'].isin(kota_pilihan)]

# Metrik
col1, col2, col3 = st.columns(3)
col1.metric("🔥 Suhu Tertinggi", f"{df_filtered['suhu'].max()} °C")
col2.metric("❄️ Suhu Terendah", f"{df_filtered['suhu'].min()} °C")
col3.metric("🌡️ Rata-rata Suhu", f"{df_filtered['suhu'].mean():.1f} °C")

# Grafik 1: Line
st.subheader("📈 Tren Suhu Bulanan")
df_filtered['bulan'] = df_filtered['tanggal'].dt.to_period('M').dt.start_time
suhu_bulanan = df_filtered.groupby('bulan')['suhu'].mean().reset_index()
fig1 = px.line(suhu_bulanan, x='bulan', y='suhu', markers=True)
fig1.update_layout(template='plotly_white', hovermode='x unified')
st.plotly_chart(fig1, use_container_width=True)

# Grafik 2: Bar
st.subheader("📊 Rata-rata Suhu per Kota")
suhu_kota = df_filtered.groupby('kota')['suhu'].mean().reset_index().sort_values('suhu', ascending=False)
fig2 = px.bar(suhu_kota, x='kota', y='suhu', color='kota', text='suhu')
fig2.update_traces(textposition='outside')
fig2.update_layout(template='plotly_white', showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

# Grafik 3: Map
st.subheader("🗺️ Peta Sebaran Suhu")
koordinat = {
    'Jakarta': (-6.2088, 106.8456), 'Surabaya': (-7.2575, 112.7521),
    'Bandung': (-6.9175, 107.6191), 'Medan': (3.5952, 98.6722),
    'Palembang': (-2.9761, 104.7754), 'Makassar': (-5.1477, 119.4327),
    'Yogyakarta': (-7.7971, 110.3688)
}
if not suhu_kota.empty:
    suhu_kota['lat'] = suhu_kota['kota'].map(lambda x: koordinat[x][0])
    suhu_kota['lon'] = suhu_kota['kota'].map(lambda x: koordinat[x][1])
    fig3 = px.scatter_mapbox(suhu_kota, lat='lat', lon='lon', size='suhu', color='suhu',
                              hover_name='kota', color_continuous_scale='RdYlBu_r',
                              size_max=50, zoom=3.5, center={'lat': -3, 'lon': 118})
    fig3.update_layout(mapbox_style='open-street-map')
    st.plotly_chart(fig3, use_container_width=True)

with st.expander("📋 Lihat Data Mentah"):
    st.dataframe(df_filtered)