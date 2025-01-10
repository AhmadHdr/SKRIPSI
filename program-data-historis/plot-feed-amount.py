import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Agar tidak tampil ke layar
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from datetime import datetime

def main():
    
    feed_file = '../data/feed_recommendations.csv'

    df = pd.read_csv(feed_file)

    # Pastikan kolom 'feed_amount' ada
    if 'feed_amount' not in df.columns:
        print("Kolom 'feed_amount' tidak ditemukan pada feed_recommendations.csv!")
        return

    # Pastikan Time dalam format datetime
    if 'Time' not in df.columns:
        print("Kolom 'Time' tidak ditemukan pada feed_recommendations.csv!")
        return

    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
    if df['Time'].isnull().all():
        print("Semua nilai Time tidak dapat dikonversi menjadi datetime!")
        return

    # Filter rentang tanggal
    start_date = datetime(2024, 8, 10)
    end_date = datetime(2024, 9, 26)
    df = df[(df['Time'] >= start_date) & (df['Time'] <= end_date)]

    if df.empty:
        print(f"Tidak ada data pada rentang {start_date} hingga {end_date}.")
        return

    # Pastikan feed_amount numerik
    df['feed_amount'] = pd.to_numeric(df['feed_amount'], errors='coerce')
    if df['feed_amount'].isnull().all():
        print("feed_amount bukan numerik atau semua nilai null!")
        return

    # Buat plot
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(df['Time'], df['feed_amount'], marker='o', linestyle='-')

    ax.set_title('Rekomendasi Jumlah Takaran dari 10 Agustus - 26 September')
    ax.set_xlabel('Waktu')
    ax.set_ylabel('Jumlah Takaran (g)')

    # Set y-ticks
    ax.set_yticks([0,10,20,30,40])

    # Set x-limit
    ax.set_xlim(start_date, end_date)

    # Set x-axis major ticks setiap 7 hari
    locator = mdates.DayLocator(interval=7)
    ax.xaxis.set_major_locator(locator)

    formatter = mdates.DateFormatter('%d %b')
    ax.xaxis.set_major_formatter(formatter)

    # Temukan nilai minimum dan maksimum
    min_value = df['feed_amount'].min()
    max_value = df['feed_amount'].max()
    min_date = df['Time'][df['feed_amount'].idxmin()]
    max_date = df['Time'][df['feed_amount'].idxmax()]

    # Tambahkan label untuk nilai minimum dan maksimum
    ax.annotate(f'Min: {min_value}g', xy=(min_date, min_value), xytext=(min_date, min_value-5),
                arrowprops=dict(facecolor='black', shrink=0.05))
    ax.annotate(f'Max: {max_value}g', xy=(max_date, max_value), xytext=(max_date, max_value+5),
                arrowprops=dict(facecolor='black', shrink=0.05))

    ax.grid(True)

    plt.tight_layout()
    plt.savefig('plot-grafik-fuzzy/feed_amount_plot.png')
    plt.close(fig)

    print("Grafik feed_amount_plot.png berhasil dibuat di folder output.")

if __name__ == '__main__':
    main()
