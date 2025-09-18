import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile


fs, data = wavfile.read("source/6.wav")
N = len(data)
T = 1.0 / fs
y = np.fft.fft(data)
x = np.fft.fftfreq(N, T)
n = (x >= 0) & (x <= 10000)
x = x[n]
y = np.abs(y[n])

plt.figure(figsize=(10, 6))
plt.plot(x, y)

plt.grid()
plt.show()
