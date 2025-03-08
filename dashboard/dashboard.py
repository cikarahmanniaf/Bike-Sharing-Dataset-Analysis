import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Analisis Bike Sharing", layout="wide")
st.sidebar.title("Navigasi & Filter")

main_data = pd.read_csv("/mount/src/bike-sharing-dataset-analysis/dashboard/main_data.csv", delimiter=";")

st.sidebar.subheader("Pilih Variabel untuk Analisis")
corr_variables = st.sidebar.multiselect("Pilih Variabel Korelasi", main_data.select_dtypes(include=[np.number]).columns.tolist(), default=["cnt"])

bins_slider = st.sidebar.slider("Jumlah Bins Histogram", min_value=5, max_value=50, value=30)

st.title("Analisis Data Bike Sharing")
st.markdown("Dashboard ini memberikan wawasan tentang tren penggunaan sepeda berdasarkan dataset Bike Sharing.")

st.subheader("Ringkasan Data")
col1, col2, col3 = st.columns(3)
col1.metric("Total Penggunaan Sepeda", main_data["cnt"].sum())
col2.metric("Rata-rata Penggunaan Harian", round(main_data["cnt"].mean(), 2))
col3.metric("Hari dengan Pemakaian Maksimum", main_data.loc[main_data['cnt'].idxmax(), 'dteday'])

st.subheader("Tampilan Data")
num_rows = st.slider("Pilih jumlah baris yang ditampilkan:", min_value=5, max_value=len(main_data), value=10, step=5)
search_query = st.text_input("Cari dalam dataset:", "")
selected_day = st.selectbox("Pilih Berdasarkan Hari:", ["Semua"] + sorted(main_data['weekday'].unique().tolist()))

filtered_data = main_data.copy()
if search_query:
    filtered_data = filtered_data[filtered_data.astype(str).apply(lambda row: search_query.lower() in row.to_string().lower(), axis=1)]
if selected_day != "Semua":
    filtered_data = filtered_data[filtered_data['weekday'] == selected_day]

st.dataframe(filtered_data.head(num_rows))

st.subheader("Statistik Deskriptif")
st.write(main_data.describe())

st.subheader("Distribusi Data")
distribution_vars = main_data.select_dtypes(include=[np.number]).columns.tolist()
selected_variable = st.selectbox("Pilih variabel untuk distribusi:", distribution_vars)
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(main_data[selected_variable], bins=bins_slider, kde=True, ax=ax, color='skyblue')
st.pyplot(fig)

st.subheader("Korelasi Antar Variabel")
numeric_data = main_data.select_dtypes(include=[np.number]).dropna(axis=1, how="all")
if len(corr_variables) > 1:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(numeric_data[corr_variables].corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
else:
    st.warning("Tidak cukup variabel untuk analisis korelasi.")

st.subheader("Tren Pemakaian Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=main_data, x=main_data.index, y='cnt', ax=ax, color='green')
st.pyplot(fig)

st.subheader("Pengaruh Cuaca Terhadap Penggunaan Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=main_data, x='weathersit', y='cnt', ax=ax, palette='coolwarm')
ax.set_xticklabels(['Clear', 'Mist', 'Light Snow/Rain', 'Heavy Rain/Snow'])
st.pyplot(fig)

st.subheader("Perbandingan Pengguna Kasual vs Terdaftar")
fig, ax = plt.subplots(figsize=(10, 5))
main_data[['casual', 'registered']].sum().plot(kind='bar', ax=ax, color=['blue', 'orange'])
ax.set_xticklabels(['Casual', 'Registered'], rotation=0)
st.pyplot(fig)

st.caption('Copyright © cikarahmanniaf')
