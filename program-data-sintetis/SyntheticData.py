'''
Data Sintetis ini dibutuhkan untuk membuat  rentang data yang lebih komprehensif
yang mencakup semua kondisi dan perubahan yang mungkin terjadi pada data aktual.

Data ini akan digunakan untuk mengukur sensitivitas variabel input terhadap variabel output.
Data akan mencakup semua nilai pada semesta pembicaraan dari variabel input.

Variabel input yang digunakan adalah:
1. Temperatur (tp)
2. pH (ph)
3. Berat Lobster (bl)

Perbandingan yang akan diukur adalah:
1. % Perubahan dari temperatur dengan kondisi ph dan berat lobster tetap terhadap jumlah takaran pakan yang direkomendasikan
2. % Perubahan dari pH dengan kondisi temperatur dan berat lobster tetap terhadap jumlah takaran pakan yang direkomendasikan
3. % Perubahan dari berat lobster dengan kondisi temperatur dan pH tetap terhadap jumlah takaran pakan yang direkomendasikan


Rentang data yang digunakan dibatasi pada batas perubahan linguistic terms pada setiap variabel input agar lebih efektif dan mengurangi redundansi data.
Nilai tetap pada variabel yang tidak berubah akan ditentukan pada batas perubahan linguistic terms pada setiap variabel input.



    temperatur_membership_params = [
        ('rendah', [14, 14, 23, 25]),
        ('normal', [23, 25, 29, 31]),
        ('tinggi', [29, 31, 40, 40])
    ]

    ph_membership_params = [
        ('asam', [4, 4, 5, 6.5]),
        ('netral', [5, 6.5, 7.5, 9]),
        ('basa', [7.5, 9, 14, 14])
    ]

'''

import numpy as np
import pandas as pd

def hitung_kombinasi(data_utama: list[float], *data_pembanding: list[float]) -> int:
    # Hitung jumlah kombinasi data
    n = len(data_utama)
    for data in data_pembanding:
        n *= len(data)

    return n

def kombinasi_data(*datas: list[float]) -> pd.DataFrame:
    # Mengkombinasikan data ke dalam array

    # Membuat grid kombinasi data
    temperature_grid, ph_grid, weight_grid = np.meshgrid(*[np.round(data, 2) for data in datas])

    # Meratakan grid menjadi array 1D 
    temperature_flat = [float(data) for data in temperature_grid.flatten()]
    ph_flat = [float(data) for data in ph_grid.flatten()] 
    weight_flat = [float(data) for data in weight_grid.flatten()]
    
    # Membuat DataFrame 
    data_sintetis = pd.DataFrame({ 
        'Temperature': temperature_flat, 
        'pH': ph_flat, 
        'LobsterWeight': weight_flat
        })
    
    return data_sintetis, zip(temperature_flat, ph_flat, weight_flat)

temp_synthetic_data = np.linspace(14, 40, 261)
ph_synthetic_data = np.linspace(4, 14, 101)

bl_synthetic_data = 100

data_sintetis, data_kombinasi = kombinasi_data(temp_synthetic_data, ph_synthetic_data, bl_synthetic_data)

for idx, data in enumerate(data_kombinasi):
    print(idx+1, data)

print(f"Jumlah kombinasi data: {data_sintetis.shape[0]}")

# Simpan ke CSV jika diperlukan 
data_sintetis.to_csv('../data/data-sintetis/complete_weight_100.csv', index=False)