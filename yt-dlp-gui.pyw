import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading

def status_callback(msg):
    status.insert(tk.END, f"{msg}\n")
    status.yview(tk.END)

def yt_dlp(url):
    yt_dlp = subprocess.Popen(
        ['yt-dlp', '-x', '-f', 'bestaudio', '--no-playlist', '--audio-format', audio_format.get(), url],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    for line in iter(yt_dlp.stdout.readline, b''):
        if line:
            decoded_line = line.decode().strip()
            status_callback(decoded_line)

    yt_dlp.wait()
    status_callback("\n\nDownload complete!")

def run():
    url = entry.get()
    entry.delete(0, tk.END)

    thread = threading.Thread(target=yt_dlp, args=(url,))
    thread.daemon = True
    thread.start()

root = tk.Tk()
root.title("yt-dlp gui")
root.geometry("600x300")

label = tk.Label(root, text="YouTube URL:")
label.pack(pady=10)

entry = tk.Entry(root, width=80)
entry.pack(pady=5)

label_audio_format = tk.Label(root, text="Audio format:")
label_audio_format.pack(pady=10)

audio_format = tk.Entry(root, width=10)
audio_format.pack(pady=5)

button = tk.Button(root, text="Get MP3", command=run)
button.pack(pady=20)

status = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=10)
status.pack(pady=5)

root.mainloop()
