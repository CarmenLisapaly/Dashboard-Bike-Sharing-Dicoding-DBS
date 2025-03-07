import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# Membaca data dari CSV dengan pengecekan keberadaan file
file_path = 'all_df.csv'
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

# Header Dashboard
st.title("Bike Sharing Data Analysis Dashboard 🚲")
st.subheader("Exploratory Data Analysis on Bike Sharing Dataset")

# Menampilkan Data Overview
st.sidebar.header("Data Overview")
st.sidebar.write("Tabel ini menunjukkan beberapa data terkait peminjaman sepeda.")
st.dataframe(all_data.head())

# Sidebar navigasi
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Visualisasi:", 
    ["Pola Penggunaan Berdasarkan Musim", 
     "Penggunaan Sepeda: Hari Kerja vs Hari Libur", 
     "Pola Penggunaan Pengguna Kasual", 
     "Clustering Pengguna Terdaftar"])

# Halaman 1: Pola Penggunaan Sepeda Berdasarkan Musim
if page == "Pola Penggunaan Berdasarkan Musim":
    season_usage = all_data.groupby('season')[cnt_col].mean()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(season_usage.index, season_usage.values, color=['#ADD8E6', '#FFD700', '#FF8C00', '#8B4513'])
    ax.set_title('Pola Penggunaan Sepeda Berdasarkan Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-rata Jumlah Peminjaman')
    ax.set_xticks(season_usage.index)
    ax.set_xticklabels(['Dingin', 'Panas', 'Semi', 'Gugur'])
    st.pyplot(fig)

# Halaman 3: Perbedaan Penggunaan Sepeda Antara Hari Kerja dan Hari Libur
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

# Halaman 4: Pola Penggunaan Sepeda oleh Pengguna Kasual
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

# Halaman 5: Clustering Pengguna Terdaftar
elif page == "Clustering Pengguna Terdaftar":
    if 'registered' in all_data.columns:
        registered_bins = [0, 50, 200, all_data['registered'].max()]
        registered_labels = ['Low', 'Medium', 'High']
        all_data['registered_cluster'] = pd.cut(all_data['registered'], bins=registered_bins, labels=registered_labels)
        registered_pattern = all_data.groupby('registered_cluster', observed=True)[cnt_col].mean().reset_index()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='registered_cluster', y=cnt_col, hue='registered_cluster', data=registered_pattern, palette='viridis', ax=ax, legend=False)
        ax.set_title('Clustering Pola Penyewaan Pengguna Terdaftar')
        ax.set_xlabel('Kelompok Pengguna Terdaftar')
        ax.set_ylabel('Rata-rata Penyewaan')
        st.pyplot(fig)
    else:
        st.error("Kolom 'registered' tidak ditemukan dalam dataset.")
