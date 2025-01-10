# PROGRAM SKRIPSI

- Nama  : Ahmad Haidar Abdullah
- NIM   : 212552018253892
- Judul : MODEL SISTEM IOT UNTUK KONTROL PAKAN OTOMATIS PADA BUDIDAYA LOBSTER AIR TAWAR BERBASIS FUZZY LOGIC

## Intro

### Penjelasan Direktori dan File

```markdown

.SKRIPSI
├── Istilah-istilah dalam fuzzy logic.txt
├── gambar-penelitian
├── README.md
├── data
│   ├── Lobster IoT.xlsx
│   ├── berat_lobster_weekly.csv
│   ├── data-sintetis
│   │   ├── data_sintetis_weight_100.csv
│   │   ├── feed_recommendations_weight_100.csv
│   │   └── inferensi_weight_100.csv
│   ├── data_terfilter.csv
│   ├── feed_recommendations.csv
│   └── inferensi.csv
├── plot-grafik-fuzzy
├── plot-pendukung
│   ├── fungsi_naik_titik_jelas.png
│   ├── fungsi_segitiga_titik_jelas.png
│   ├── fungsi_trapesium_titik_jelas.png
│   ├── fungsi_turun_titik_jelas.png
│   ├── fuzzy_membership_functions.png
│   └── membership_functions_part.py
├── program-data-historis
│   ├── addFeedAmount.py
│   ├── plot-feed-amount.py
│   └── plot-setiap-waktu-pemberian-pakan.py
├── program-data-sintetis
│   ├── HitungSensitivitas.ipynb
│   ├── SyntheticData.py
│   ├── addFeedAmountSyntheticData.py
│   └── plot-data-sintetis
│       ├── Pengaruh Temperatur terhadap Takaran Pakan (pH = 8, LobsterWeight = 100).png
│       ├── Pengaruh pH terhadap Takaran Pakan (Temperature = 24, LobsterWeight = 100).png
│       ├── Visualisasi Temperature pada Rentang 23°C - 25°C dan 29°C - 31°C.png
│       └── Visualisasi pH pada Rentang 5 - 6,5 dan 7,5 - 9.png
└── requirements.txt
```

- Program untuk mengolah data historis terdapat pada direktori `program-data-historis`
- Program untuk mengolah data sintetis terdapat pada direktori `program-data-sintetis`
- Data yang digunakan terdapat pada direktori `data` dan `data/data-sintetis`
- Plot dari hasil data histori terdapat pada `program-data-historis/plot-grafik-fuzzy`
- Plot dari hasil data sintetis terdapat pada `program-data-sintetis/plot-data-sintetis`
- Istilah dan Langkah - langkah pengerjaan penelitian terdapat pada `istilah dan langkah-langkah.txt`
- Libraries python yang saya gunakan terdapat pada `requirements.txt`

### Persiapan Environment
Untuk menjalankan program ini, Anda perlu menginstal library yang terdapat pada `requirements.txt`
dengan menggunakan perintah berikut:

> pip install -r requirements.txt

atau jika ingin menggunakan virtual environment maka buat virtual environment terlebih dahulu dengan perintah:

> python -m venv env
> source env/bin/activate (untuk Linux/Mac)
> env\Scripts\activate (untuk Windows)

Menjalankan program menggunkana virtual environment sangat disarankan untuk menghindari konflik versi dengan libraries
yang terinstall pada environment global.