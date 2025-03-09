import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# Membaca data dari CSV dengan pengecekan keberadaan file
file_path = 'dashboard/all_df.csv'
try:
    all_data = pd.read_csv(file_path)
except FileNotFoundError:
    st.error(f"Error: File '{file_path}' tidak ditemukan. Pastikan file ada di lokasi yang benar.")
    st.stop()

# Pastikan kolom 'cnt' ada, jika tidak, cari alternatifnya
if 'cnt' in all_data.columns:
    cnt_col = 'cnt'
elif 'cnt_day' in all_data.columns:
    cnt_col = 'cnt_day'
elif 'cnt_hour' in all_data.columns:
    cnt_col = 'cnt_hour'
else:
    st.error("Error: Tidak ada kolom 'cnt', 'cnt_day', atau 'cnt_hour' dalam dataset.")
    st.stop()

# Hapus nilai NaN pada kolom yang digunakan untuk filtering
all_data.dropna(subset=['season', 'weathersit'], inplace=True)

# Header Dashboard
st.title("Bike Sharing Data Analysis Dashboard 🚲")
st.subheader("Exploratory Data Analysis on Bike Sharing Dataset")

# Sidebar Filtering
st.sidebar.header("Filter Data")

# Filter berdasarkan Musim
season_options = all_data['season'].dropna().unique().tolist()
season_filter = st.sidebar.multiselect("Pilih Musim:", season_options, default=season_options)
all_data = all_data[all_data['season'].isin(season_filter)]

# Menampilkan Data Overview
st.sidebar.header("Data Overview")
st.sidebar.write("Tabel ini menunjukkan beberapa data terkait peminjaman sepeda.")
st.dataframe(all_data.head())

# Sidebar navigasi
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Visualisasi:", 
    ["Pola Penggunaan Berdasarkan Musim", 
     "Penggunaan Sepeda: Hari Kerja vs Hari Libur", 
     "Pola Penggunaan Pengguna Kasual"])

# Halaman 1: Pola Penggunaan Sepeda Berdasarkan Musim
if page == "Pola Penggunaan Berdasarkan Musim":
    season_usage = all_data.groupby('season')[cnt_col].mean()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(season_usage.index, season_usage.values, color=['#ADD8E6', '#FFD700', '#FF8C00', '#8B4513'])
    ax.set_title('Pola Penggunaan Sepeda Berdasarkan Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-rata Jumlah Peminjaman')
    ax.set_xticks(season_usage.index)
    season_labels = {1: 'Semi', 2: 'Panas', 3: 'Gugur', 4: 'Dingin'}
    ax.set_xticklabels([season_labels.get(season, str(season)) for season in season_usage.index])
    st.pyplot(fig)

# Halaman 2: Perbedaan Penggunaan Sepeda Antara Hari Kerja dan Hari Libur
elif page == "Penggunaan Sepeda: Hari Kerja vs Hari Libur":
    if 'workingday' in all_data.columns:
        workday_usage = all_data.groupby('workingday')[cnt_col].mean()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(workday_usage.index, workday_usage.values, color=['#FF6347', '#32CD32'])
        ax.set_title('Perbedaan Penggunaan Sepeda Antara Hari Kerja dan Hari Libur')
        ax.set_xlabel('Hari Kerja')
        ax.set_ylabel('Rata-rata Jumlah Peminjaman')
        ax.set_xticks([0, 1], labels=['Hari Libur', 'Hari Kerja'])
        st.pyplot(fig)
    else:
        st.error("Kolom 'workingday' tidak ditemukan dalam dataset.")

# Halaman 3: Pola Penggunaan Sepeda oleh Pengguna Kasual
elif page == "Pola Penggunaan Pengguna Kasual":
    if 'casual' in all_data.columns and 'hr' in all_data.columns:
        casual_pattern = all_data.groupby('hr')['casual'].mean()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(casual_pattern.index, casual_pattern.values, color='#FF8C00')
        ax.set_title('Pola Penggunaan Sepeda oleh Pengguna Kasual')
        ax.set_xlabel('Jam')
        ax.set_ylabel('Rata-rata Peminjaman')
        ax.set_xticks(range(24))
        st.pyplot(fig)
    else:
        st.error("Kolom 'casual' atau 'hr' tidak ditemukan dalam dataset.")
