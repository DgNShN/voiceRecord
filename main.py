import subprocess
import threading
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Global değişkenler
output_file_var = None
duration_entry = None
start_button = None
stop_button = None
exit_button = None
ffmpeg_process = None


# Ekran ve ses kaydı için komut (ffmpeg kullanarak)
def record_screen_with_audio(output_file, duration):
    global ffmpeg_process

    command = [
        'ffmpeg',
        '-y',  # Overwrite output file if exists
        '-f', 'gdigrab',  # Windows ekran kaydı için
        '-framerate', '30',  # Kayıt hızı
        '-i', 'desktop',  # Ekran kaynağı
        '-f', 'dshow',  # Windows DirectShow kullanarak ses kaydı
        '-i', 'audio=Microphone Array (Dijital Mikrofonlar için Intel® Smart Sound Teknolojisi)',  # Mikrofon cihazı
        '-t', str(duration),  # Kayıt süresi
        '-vcodec', 'libx264',  # Video codec
        '-acodec', 'aac',  # Ses codec
        '-pix_fmt', 'yuv420p',  # Pixel formatı
        output_file  # Çıktı dosyası
    ]

    ffmpeg_process = subprocess.Popen(command)


# Arka planda kaydı başlatmak için bir thread oluşturuluyor
def start_recording(output_file, duration):
    global ffmpeg_process
    record_thread = threading.Thread(target=record_screen_with_audio, args=(output_file, duration))
    record_thread.start()
    return record_thread


# Kaydı durdurmak için
def stop_recording():
    global ffmpeg_process
    if ffmpeg_process:
        ffmpeg_process.terminate()
        ffmpeg_process = None


# Kullanıcıdan kaydedilecek dosya konumunu seçmesini sağlayan fonksiyon
def browse_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".mkv", filetypes=[("MKV files", "*.mkv")])
    if file_path:
        output_file_var.set(file_path)


# Kayıt tamamlandığında bilgi mesajı gösterme
def show_completion_message():
    messagebox.showinfo("Recording Complete", "The recording has been completed.")


# GUI ile kayıt süresi ve dosya konumunu seçme
def start_gui():
    global output_file_var, duration_entry, start_button, stop_button, exit_button

    # Tkinter arayüzü
    root = tk.Tk()
    root.title("Screen Recorder with Audio")

    # Global değişkenler
    output_file_var = tk.StringVar()

    # Dosya seçme
    tk.Label(root, text="Output File:").grid(row=0, column=0, padx=10, pady=5)
    output_entry = tk.Entry(root, textvariable=output_file_var, width=40)
    output_entry.grid(row=0, column=1, padx=10, pady=5)
    browse_button = tk.Button(root, text="Browse", command=browse_output_file)
    browse_button.grid(row=0, column=2, padx=10, pady=5)

    # Süre girişi
    tk.Label(root, text="Duration (seconds):").grid(row=1, column=0, padx=10, pady=5)
    duration_entry = tk.Entry(root, width=10)
    duration_entry.grid(row=1, column=1, padx=10, pady=5)

    # Kayıt başlat ve durdur düğmeleri
    start_button = tk.Button(root, text="Start Recording", command=start_record)
    start_button.grid(row=2, column=0, padx=10, pady=10)

    stop_button = tk.Button(root, text="Stop Recording", command=stop_record, state=tk.DISABLED)
    stop_button.grid(row=2, column=1, padx=10, pady=10)

    # Çıkış düğmesi
    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.grid(row=2, column=2, padx=10, pady=10)

    root.mainloop()


# Kayıt başlatma fonksiyonu
def start_record():
    output_file = output_file_var.get()
    duration = int(duration_entry.get())
    start_recording(output_file, duration)
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

    # Kaydın süresi dolduğunda otomatik olarak durdurma ve uyarı gösterme
    threading.Timer(duration, lambda: [stop_record(), show_completion_message()]).start()


# Kaydı durdurma fonksiyonu
def stop_record():
    stop_recording()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)


# Programı başlat
if __name__ == "__main__":
    start_gui()
