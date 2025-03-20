import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import os
import sys

def status_callback(msg):
    status.insert(tk.END, f"{msg}\n")
    status.yview(tk.END)

def yt_dlp(url):
    yt_dlp = subprocess.Popen(
        [yt_dlp_path, '-x', '-f', 'bestaudio', '--no-playlist', '--audio-format', 'mp3', url],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, creationflags=subprocess.CREATE_NO_WINDOW
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

def get_exe_path(file):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, file)
    return os.path.join(os.path.dirname(__file__), file)



yt_dlp_path = get_exe_path("yt-dlp.exe")
ffmpeg_path = get_exe_path("ffmpeg.exe")

env = os.environ.copy()
env["PATH"] = f"{os.path.dirname(ffmpeg_path)};{env['PATH']}"

root = tk.Tk()
root.title("Inconspicuous bitcoin miner... I mean YT to MP3")
root.geometry("600x300")

label = tk.Label(root, text="YouTube URL:")
label.pack(pady=10)

entry = tk.Entry(root, width=80)
entry.pack(pady=5)

button = tk.Button(root, text="Get MP3", command=run)
button.pack(pady=20)

status = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=10)
status.pack(pady=5)

root.mainloop()
