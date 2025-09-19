import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


wav_files = [f for f in os.listdir("source") if f.endswith(".wav")]

def local_max_3(x, y):
    y_copy = y.copy()
    list_max = []
    for _ in range(3):
        i = np.argmax(y_copy)
        list_max.append((x[i], y_copy[i]))
        mask = (x > x[i] - 150) & (x < x[i] + 150)
        y_copy[mask] = 0
    return list_max

def plot_fft(filename):
    fs, data = wavfile.read("source/" + filename)
    N = len(data)
    T = 1.0 / fs
    y = np.fft.fft(data)
    x = np.fft.fftfreq(N, T)
    n = (x >= 0) & (x <= 10000)
    x_plot = x[n]
    y_plot = np.abs(y[n])
    y_db = 20 * np.log10(y_plot + 1e-12)
    
    list_max = local_max_3(x_plot, y_plot)
    colors = ["red", "green", "blue"]

    pl[0].clear()
    pl[1].clear()
    
    pl[0].plot(x_plot, y_db)
    for i in range(3):
        freq, amp = list_max[i]
        db_val = 20 * np.log10(amp)
        pl[0].plot(freq, db_val, "o", color=colors[i])
    pl[0].set_title("Spectrum (dB)")
    pl[0].set_xlabel("Frequency (Hz)")
    pl[0].set_ylabel("Amplitude (dB)")
    pl[0].grid()
    
    pl[1].plot(x_plot, y_plot)
    for i in range(3):
        freq, amp = list_max[i]
        pl[1].plot(freq, amp, "o", color=colors[i])
    pl[1].set_title("Raw Spectrum")
    pl[1].set_xlabel("Frequency (Hz)")
    pl[1].set_ylabel("Amplitude")
    pl[1].grid()

    for i in range(3):
        freq, _ = list_max[i]
        freq_labels[i].config(text=f"{freq:.1f} Hz", fg=colors[i])

    canvas.draw()

root = tk.Tk()
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)
menu_frame = tk.Frame(frame)
menu_frame.pack(side=tk.LEFT, padx=10)
tk.Label(menu_frame, text="Audio file:").pack(pady=5)
selected_file = tk.StringVar()
selected_file.set(wav_files[0])
dropdown = ttk.Combobox(menu_frame, textvariable=selected_file, values=wav_files, state="readonly")
dropdown.pack(pady=5)

freq_labels = [tk.Label(menu_frame, text="") for _ in range(3)]
for lbl in freq_labels:
    lbl.pack(pady=2)

plot_frame = tk.Frame(frame)
plot_frame.pack(side=tk.RIGHT)
fig, pl = plt.subplots(1, 2, figsize=(10, 5))
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack()

def on_select(event):
    plot_fft(selected_file.get())

dropdown.bind("<<ComboboxSelected>>", on_select)
plot_fft(selected_file.get())

root.mainloop()
