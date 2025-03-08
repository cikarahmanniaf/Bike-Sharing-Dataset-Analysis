# Dashboard Analisis Data

## Setup Environment (Pilih salah satu)

### 1. Menggunakan Virtual Environment (venv)
```sh
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 2️. Menggunakan Anaconda
```sh
conda create --name main-ds python=3.9.2
conda activate main-ds
pip install -r requirements.txt
```

### 3. Menggunakan Pipenv
```sh
mkdir submission
cd submission/dashboard, submission/data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Menjalankan Streamlit App

Setelah environment siap, jalankan aplikasi dengan perintah berikut:
```sh
cd dashboard
streamlit run dashboard.py
```

## Struktur Direktori
```
submission
├───dashboard
│   ├───dashboard.py
├───data
│   ├───day.csv
│   └───hour.csv
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt
```

## Deploy ke Streamlit Cloud
Untuk melakukan deploy ke **Streamlit Community Cloud**, ikuti langkah-langkah berikut:

1. **Upload proyek ke GitHub**
   - Pastikan semua file penting sudah ada di repositori GitHub.
   
2. **Login ke [Streamlit Cloud](https://share.streamlit.io)**
   - Sign in menggunakan akun GitHub.
   
3. **Deploy aplikasi**
   - Klik tombol **'New app'** dan pilih repositori yang berisi dashboard-mu.
   - Isi informasi aplikasi:
     - Branch: `main`
     - File utama: `dashboard/dashboard.py`
   - Klik **Deploy**.

4. **Dapatkan URL dashboard**
   - Setelah sukses, salin URL aplikasi dan simpan dalam `url.txt`.

