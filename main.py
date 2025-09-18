import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


wav_files = [f for f in os.listdir("source") if f.endswith(".wav")]

def plot_fft(filename):
    fs, data = wavfile.read("source/"+filename)
    N = len(data)
    T = 1.0 / fs
    y = np.fft.fft(data)
    x = np.fft.fftfreq(N, T)
    n = (x >= 0) & (x <= 10000)
    x_plot = x[n]
    y_plot = np.abs(y[n])
    y_db = 20 * np.log10(y_plot)
    pl[0].clear()
    pl[1].clear()
    pl[0].plot(x_plot, y_db)
    pl[1].plot(x_plot, y_plot)
    canvas.draw()

root = tk.Tk()
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)
menu_frame = tk.Frame(frame)
menu_frame.pack(side=tk.LEFT, padx=10)
tk.Label(menu_frame, text="Audio file :").pack(pady=5)
selected_file = tk.StringVar()
selected_file.set(wav_files[0])
dropdown = ttk.Combobox(menu_frame, textvariable=selected_file, values=wav_files, state="readonly")
dropdown.pack(pady=5)
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
