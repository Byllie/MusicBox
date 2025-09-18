import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile


fs, data = wavfile.read("source/1.wav")
N = len(data)
T = 1.0 / fs
y = np.fft.fft(data)
x = np.fft.fftfreq(N, T)
n = (x >= 0) & (x <= 10000)
x = x[n]
y = np.abs(y[n])
y_db = 20 * np.log10(y) 
plt.figure(figsize=(10, 6))
plt.plot(x, y_db)

plt.grid()
plt.show()
