import numpy as np
import matplotlib.pyplot as plt

# Fungsi Naik (Increasing Function)
def fungsi_naik(x, a, b):
    return np.where(x <= a, 0, np.where(x >= b, 1, (x - a) / (b - a)))

# Fungsi Turun (Decreasing Function)
def fungsi_turun(x, a, b):
    return np.where(x <= a, 1, np.where(x >= b, 0, (b - x) / (b - a)))

# Fungsi Segitiga (Triangular Function)
def fungsi_segitiga(x, a, b, c):
    return np.where(x <= a, 0, 
                    np.where(x <= b, (x - a) / (b - a),
                             np.where(x <= c, (c - x) / (c - b), 0)))

# Fungsi Trapesium (Trapezoidal Function)
def fungsi_trapesium(x, a, b, c, d):
    return np.where(x <= a, 0,
                    np.where(x <= b, (x - a) / (b - a),
                             np.where(x <= c, 1,
                                      np.where(x <= d, (d - x) / (d - c), 0))))

# Fungsi untuk menambahkan titik dengan label yang jelas
def tambah_titik_dengan_label(x, y, label, offset_x=0, offset_y=0, color='black'):
    plt.scatter(x, y, color=color, zorder=5)  # Tambahkan titik hitam yang jelas
    for i, txt in enumerate(label):
        plt.annotate(txt, (x[i], y[i]), textcoords="offset points", xytext=(offset_x, offset_y), ha='center', fontsize=10,
                     bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"))

# Range untuk plot
x = np.linspace(0, 10, 500)

# Plot Fungsi Naik
plt.figure(figsize=(6, 4))
y_naik = fungsi_naik(x, 3, 7)
plt.plot(x, y_naik, label='Fungsi Naik')
plt.title('Fungsi Naik')
plt.xlabel('x')
plt.ylabel('Keanggotaan (\u03BC)')
plt.grid(True)
plt.legend()
tambah_titik_dengan_label([3, 7], [0, 1], ['a', 'b'], offset_y=-15, color='black')
plt.savefig("fungsi_naik_titik_jelas.png")
plt.close()

# Plot Fungsi Turun
plt.figure(figsize=(6, 4))
y_turun = fungsi_turun(x, 3, 7)
plt.plot(x, y_turun, label='Fungsi Turun', color='orange')
plt.title('Fungsi Turun')
plt.xlabel('x')
plt.ylabel('Keanggotaan (\u03BC)')
plt.grid(True)
plt.legend()
tambah_titik_dengan_label([3, 7], [1, 0], ['a', 'b'], offset_y=15, color='black')
plt.savefig("fungsi_turun_titik_jelas.png")
plt.close()

# Plot Fungsi Segitiga
plt.figure(figsize=(6, 4))
y_segitiga = fungsi_segitiga(x, 2, 5, 8)
plt.plot(x, y_segitiga, label='Fungsi Segitiga', color='green')
plt.title('Fungsi Segitiga')
plt.xlabel('x')
plt.ylabel('Keanggotaan (\u03BC)')
plt.grid(True)
plt.legend()
tambah_titik_dengan_label([2, 5, 8], [0, 1, 0], ['a', 'b', 'c'], offset_y=-15, color='black')
plt.savefig("fungsi_segitiga_titik_jelas.png")
plt.close()

# Plot Fungsi Trapesium
plt.figure(figsize=(6, 4))
y_trapesium = fungsi_trapesium(x, 2, 4, 6, 8)
plt.plot(x, y_trapesium, label='Fungsi Trapesium', color='red')
plt.title('Fungsi Trapesium')
plt.xlabel('x')
plt.ylabel('Keanggotaan (\u03BC)')
plt.grid(True)
plt.legend()
tambah_titik_dengan_label([2, 4, 6, 8], [0, 1, 1, 0], ['a', 'b', 'c', 'd'], offset_y=-15, color='black')
plt.savefig("fungsi_trapesium_titik_jelas.png")
plt.close()

