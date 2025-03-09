import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Analisis Bike Sharing", layout="wide")
st.sidebar.title("Navigasi & Filter")

main_data = pd.read_csv("main_data.csv", delimiter=";")

st.sidebar.subheader("Pilih Musim dan Cuaca untuk Analisis")
season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weather_labels = {1: "Clear", 2: "Mist + Cloudy", 3: "Light Snow/Rain", 4: "Heavy Rain/Snow+Fog"}

main_data["season_label"] = main_data["season"].map(season_labels)
main_data["weather_label"] = main_data["weathersit"].map(weather_labels)

selected_season = st.sidebar.selectbox("Pilih Musim:", ["Semua"] + list(season_labels.values()))
selected_weather = st.sidebar.selectbox("Pilih Cuaca:", ["Semua"] + list(weather_labels.values()))

filtered_data = main_data.copy()
if selected_season != "Semua":
    filtered_data = filtered_data[filtered_data["season_label"] == selected_season]
if selected_weather != "Semua":
    filtered_data = filtered_data[filtered_data["weather_label"] == selected_weather]

st.title("Analisis Data Bike Sharing")
st.markdown("Dashboard ini memberikan wawasan tentang tren penggunaan sepeda berdasarkan dataset Bike Sharing.")

if filtered_data.empty:
    st.warning(f"Tidak ada data tercatat untuk Musim **{selected_season}** dan Cuaca **{selected_weather}**.")
else:
    st.subheader("Ringkasan Data")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Penggunaan Sepeda", filtered_data["cnt"].sum())
    col2.metric("Rata-rata Penggunaan Harian", round(filtered_data["cnt"].mean(), 2))
    col3.metric("Hari dengan Pemakaian Maksimum", filtered_data.loc[filtered_data['cnt'].idxmax(), 'dteday'])

    st.subheader("Tampilan Data")
    num_rows = st.slider("Pilih jumlah baris yang ditampilkan:", min_value=5, max_value=len(filtered_data), value=10, step=5)
    search_query = st.text_input("Cari dalam dataset:", "")
    st.dataframe(filtered_data.head(num_rows))
    
    st.subheader("Statistik Deskriptif")
    st.write(filtered_data.describe())

    st.subheader("Pengaruh Suhu terhadap Peminjaman Sepeda")
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.scatterplot(x="temp", y="casual", data=filtered_data, alpha=0.6, color="teal", label="Kasual")
    sns.scatterplot(x="temp", y="registered", data=filtered_data, alpha=0.6, color="coral", label="Terdaftar")
    plt.xlabel("Suhu (Normalized)")
    plt.ylabel("Jumlah Peminjaman")
    plt.title("Pengaruh Suhu terhadap Peminjaman Sepeda")
    plt.legend()
    st.pyplot(fig)

    st.subheader("Tren Peminjaman Berdasarkan Musim dan Cuaca")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    season_counts = filtered_data.groupby("season_label")["cnt"].mean().reindex(season_labels.values()).tolist()
    ax1.bar(season_labels.values(), season_counts, color=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"])
    ax1.set_title("Rata-rata Peminjaman Sepeda per Musim")
    ax1.set_ylabel("Rata-rata Jumlah Peminjaman")
    ax1.grid(axis="y", linestyle="--", alpha=0.7)

    weather_counts = filtered_data.groupby("weather_label")["cnt"].mean().reindex(weather_labels.values(), fill_value=0).tolist()
    ax2.pie(weather_counts, labels=weather_labels.values(), autopct="%1.1f%%", colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"])
    ax2.set_title("Distribusi Peminjaman Berdasarkan Kondisi Cuaca")

    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Tren Peminjaman Sepeda per Bulan")
    monthly_trend = filtered_data.groupby(["yr", "mnth"])[["casual", "registered"]].mean().reset_index()
    monthly_trend["Bulan"] = monthly_trend["yr"].astype(str) + "-" + monthly_trend["mnth"].astype(str)
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(monthly_trend["Bulan"], monthly_trend["casual"], marker='o', color="#66b3ff", label="Kasual")
    ax.plot(monthly_trend["Bulan"], monthly_trend["registered"], marker='o', color="#ff9999", label="Terdaftar")
    ax.set_title("Tren Peminjaman Sepeda per Bulan (Kasual vs Terdaftar)")
    ax.set_ylabel("Rata-rata Jumlah Peminjaman")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.caption('Copyright © cikarahmanniaf')
