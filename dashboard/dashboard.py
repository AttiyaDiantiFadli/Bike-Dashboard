import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import plotly.express as px

sns.set(style='dark')

# Load Data
file_path = "dashboard/all_data.csv"
bike_df = pd.read_csv(file_path)

# Ubah semua nama kolom menjadi lowercase
bike_df.columns = bike_df.columns.str.lower()

# Pastikan nama kolom yang benar digunakan
if "cnt_x" in bike_df.columns and "cnt_y" in bike_df.columns:
    cnt_column = "cnt_x"  # Pilih salah satu, bisa diubah ke "cnt_y" jika perlu
elif "cnt_x" in bike_df.columns:
    cnt_column = "cnt_x"
elif "cnt_y" in bike_df.columns:
    cnt_column = "cnt_y"
else:
    st.error("Kolom 'cnt' tidak ditemukan dalam dataset.")
    st.stop()

# Konversi kolom tanggal
bike_df["dteday"] = pd.to_datetime(bike_df["dteday"])
bike_df.sort_values(by="dteday", inplace=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9033/9033633.png")
    
    st.subheader("📍 Kontak Kami:")
    st.write("📌 **Alamat:** Musi Rawas Utara")
    st.write("📞 **Telepon:** +62 857-4092-2279")
    st.write("✉️ **Email:** attiyadiantifadli@gmail.com")

# Dashboard Header
st.header('Bike Rental Dashboard 🚴‍♂️')
st.write("Selamat datang di layanan penyewaan sepeda terbaik. Kami menawarkan berbagai jenis sepeda untuk berbagai kebutuhan Anda, mulai dari sepeda standar untuk perjalanan santai hingga sepeda listrik dan sepeda gunung untuk petualangan yang lebih menantang. Layanan kami tersedia setiap hari dengan harga terjangkau dan kualitas terbaik.")

# Harga Sewa
st.subheader("Harga Sewa Sepeda")
st.write("Sepeda Standar: Rp. 15.000/jam")
st.write("Sepeda Listrik: Rp. 25.000/jam")
st.write("Sepeda Gunung: Rp. 40.000/jam")

# Statistik Penyewaan
st.subheader('📊 Statistik Penyewaan')
col1, col2 = st.columns(2)
with col1:
    total_orders = bike_df[cnt_column].sum()
    st.metric("Total Penyewaan", value=total_orders)
with col2:
    total_revenue = format_currency(total_orders * 15000, "IDR", locale='id_ID')  # Harga rata-rata Rp. 15.000
    st.metric("Total Revenue", value=total_revenue)

# Grafik Penyewaan Harian
st.subheader('📅 Penyewaan Harian')
fig = px.line(bike_df, x="dteday", y=cnt_column, markers=True, title="Tren Penyewaan Harian")
st.plotly_chart(fig)

# Penyewaan Berdasarkan Musim
st.subheader("🌦️ Penyewaan Berdasarkan Musim")
byseason_df = bike_df.groupby("season").agg({cnt_column: "sum"}).reset_index()
fig = px.bar(byseason_df, x="season", y=cnt_column, color="season", title="Total Penyewaan per Musim")
st.plotly_chart(fig)

# Penyewaan Sepeda: Hari Kerja vs Akhir Pekan
st.subheader("📆 Penyewaan: Hari Kerja vs Akhir Pekan")
workday_df = bike_df.groupby("workingday").agg({cnt_column: "sum"}).reset_index()
workday_df["workingday"] = workday_df["workingday"].map({0: "Akhir Pekan", 1: "Hari Kerja"})
fig = px.pie(workday_df, names="workingday", values=cnt_column, title="Perbandingan Penyewaan")
st.plotly_chart(fig)

# Penyewaan Sepeda Berdasarkan Jam dalam Sehari
st.subheader("⏰ Penyewaan Berdasarkan Jam")
hourly_df = bike_df.groupby("hr").agg({cnt_column: "sum"}).reset_index()
fig = px.bar(hourly_df, x="hr", y=cnt_column, title="Jumlah Penyewaan per Jam", color="hr")
st.plotly_chart(fig)

st.caption('Copyright © Attiya Dianti Fadli 2025')
