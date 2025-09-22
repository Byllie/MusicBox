import os
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sounddevice as sd

# List available audio files 
wav_files = [f for f in os.listdir("source") if f.endswith(".wav")]
exclude_options = [50, 100, 150, 200, 250, 300, 350, 400]

def zero_padding(data, fs, sec):
    """Pad the audio signal with zeros to reach a fixed duration (sec)."""
    pad = np.zeros(sec*fs, dtype=data.dtype)
    pad[:len(data)] = data
    return pad

def local_max_5(x, y, exclude_hz):
    """Find the top 5 local maxima in the spectrum with exclusion zones."""
    y_copy = y.copy()
    list_max = []
    for _ in range(5):
        i = np.argmax(y_copy)
        list_max.append((x[i], y_copy[i]))
        # Exclude a band around the current maximum
        mask = (x > x[i] - exclude_hz) & (x < x[i] + exclude_hz)
        y_copy[mask] = 0
    return list_max

def plot_fft(filename):
    """Compute FFT of selected file and plot both raw and dB spectrums."""
    fs, data = wavfile.read("source/" + filename)
    data = zero_padding(data, fs, 4)  # Pad to 4 second
    N = len(data)
    T = 1.0 / fs
    y = np.fft.fft(data)
    x = np.fft.fftfreq(N, T)
    n = (x >= 0) & (x <= 10000)
    x_plot = x[n]
    y_plot = np.abs(y[n])
    y_db = 20 * np.log10(y_plot + 1e-12)
    
    exclude_hz = int(selected_exclude.get())
    list_max = local_max_5(x_plot, y_plot, exclude_hz)
    max_amp = list_max[0][1]
    colors = ["red", "green", "blue", "orange", "purple"]

    # Clear previous plots
    pl[0].clear()
    pl[1].clear()

    # Plot dB spectrum
    pl[0].plot(x_plot, y_db)
    for i in range(5):
        freq, amp = list_max[i]
        db_val = 20 * np.log10(amp)
        pl[0].plot(freq, db_val, "o", color=colors[i])
    pl[0].set_title("Spectrum (dB)")
    pl[0].set_xlabel("Frequency (Hz)")
    pl[0].set_ylabel("Amplitude (dB)")
    pl[0].grid()

    # Plot raw spectrum
    pl[1].plot(x_plot, y_plot)
    for i in range(5):
        freq, amp = list_max[i]
        pl[1].plot(freq, amp, "o", color=colors[i])
    pl[1].set_title("Raw Spectrum")
    pl[1].set_xlabel("Frequency (Hz)")
    pl[1].set_ylabel("Amplitude")
    pl[1].grid()

    # Update frequency labels
    for i in range(5):
        freq, amp = list_max[i]
        diff_db = 20 * np.log10(amp / max_amp + 1e-12)
        freq_labels[i].config(text=f"{freq:.1f} Hz ({diff_db:.1f} dB)", fg=colors[i])

    canvas.draw()

def play_audio():
    """Play the selected audio file using sounddevice."""
    fs, data = wavfile.read("source/" + selected_file.get())
    sd.stop()
    sd.play(data, fs)

# --- GUI setup ---
root = tk.Tk()
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

menu_frame = tk.Frame(frame)
menu_frame.pack(side=tk.LEFT, padx=10)

# Button to play audio
btn = tk.Button(menu_frame, text="🔊", command=play_audio)
btn.pack(pady=5)

# Audio file dropdown
tk.Label(menu_frame, text="Audio file:").pack(pady=5)
selected_file = tk.StringVar()
selected_file.set(wav_files[0])
dropdown = ttk.Combobox(menu_frame, textvariable=selected_file, values=wav_files, state="readonly")
dropdown.pack(pady=5)

# Exclusion bandwidth dropdown
tk.Label(menu_frame, text="Exclude around max (Hz):").pack(pady=5)
selected_exclude = tk.StringVar()
selected_exclude.set(str(exclude_options[2]))
exclude_dropdown = ttk.Combobox(menu_frame, textvariable=selected_exclude, values=exclude_options, state="readonly")
exclude_dropdown.pack(pady=5)

# Frequency labels for the 5 maxima
freq_labels = [tk.Label(menu_frame, text="") for _ in range(5)]
for lbl in freq_labels:
    lbl.pack(pady=2)

# Plotting area with two subplots
plot_frame = tk.Frame(frame)
plot_frame.pack(side=tk.RIGHT)
fig, pl = plt.subplots(1, 2, figsize=(10, 5))
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack()

def on_select(event=None):
    """Callback to redraw plot when a new file or exclusion value is selected."""
    plot_fft(selected_file.get())

# Bind events for dropdowns
dropdown.bind("<<ComboboxSelected>>", on_select)
exclude_dropdown.bind("<<ComboboxSelected>>", on_select)

# Initial plot
plot_fft(selected_file.get())

root.mainloop()
