import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

st.set_page_config(page_title="Dashboard Analisis Penyewaan Sepeda", layout="wide")

# Meng load data
@st.cache_data
def load_data():
    # file_path = "dashboard/df_day.csv"
    file_path = os.path.join(os.path.dirname(__file__), "df_day.csv")
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error("File tidak ditemukan. Pastikan file tersedia di lokasi yang benar.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# Mengecek apakah kolom yang dimaksud ada dalam dataset
if 'season' not in df.columns or 'dteday' not in df.columns or 'yr' not in df.columns:
    st.error("Kolom yang diperlukan tidak ditemukan dalam dataset.")
    st.stop()

# Judul
st.title("📊 Dashboard Analisis Penyewaan Sepeda")
st.write("### Data Penyewaan Sepeda Tahun 2011 dan 2012")

# Sidebar tahun, musim, dan bulan
st.sidebar.header("Filter Rentang Waktu")

year_option = st.sidebar.radio("Pilih Tahun:", ['2011 & 2012', '2011', '2012'])
season_option = st.sidebar.multiselect("Pilih Musim:", ['Spring', 'Summer', 'Fall', 'Winter'], default=['Spring', 'Summer', 'Fall', 'Winter'])
month_option = st.sidebar.multiselect("Pilih Bulan:", list(range(1, 13)), default=list(range(1, 13)))

# Mapping dan filter data
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
df['season'] = df['season'].map(season_mapping)
df['season'] = pd.Categorical(df['season'], categories=["Spring", "Summer", "Fall", "Winter"], ordered=True)
df['month'] = pd.to_datetime(df['dteday']).dt.month
df['yr'] = df['yr'].map({0: 2011, 1: 2012})

if year_option != '2011 & 2012':
    df = df[df['yr'] == int(year_option)]
df = df[df['season'].isin(season_option)]
df = df[df['month'].isin(month_option)]

# Visualisasi 1: Penyewaan Sepeda Berdasarkan Musim
st.subheader("Perkembangan Penyewaan Sepeda per Musim")
seasonal_data = df.groupby(['season', 'yr'])['cnt'].sum().reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='season', y='cnt', hue='yr', data=seasonal_data, palette='coolwarm', ax=ax)
plt.xlabel("Musim")
plt.ylabel("Total Penyewaan")
plt.title("Total Penyewaan Sepeda per Musim")
st.pyplot(fig)

# Insight Visualisasi 1
st.markdown(
    "\n✅ **Musim Semi (Spring) menunjukkan lonjakan signifikan dibandingkan tahun sebelumnya**."
    "\n✅ **Musim Gugur (Fall) memiliki jumlah penyewaan tertinggi**."
)

# Visualisasi 2: Tren Penyewaan Sepeda per Bulan
st.subheader("Tren Penyewaan Sepeda per Bulan")
monthly_data = df.groupby(['month', 'yr'])['cnt'].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='month', y='cnt', hue='yr', data=monthly_data, marker='o', palette='coolwarm', ax=ax)
plt.xlabel("Bulan")
plt.ylabel("Total Penyewaan")
plt.title("Tren Penyewaan Sepeda per Bulan")
st.pyplot(fig)

# Insight Visualisasi 2
st.markdown(
    "\n✅ **Lonjakan besar terjadi di awal tahun, terutama Januari hingga Maret**."
    "\n✅ **Terjadi penurunan tren di akhir tahun (Oktober - Desember)**."
)

# Menampilkan DataFrame
st.subheader("📜 Data Penyewaan Sepeda")
st.dataframe(df)
