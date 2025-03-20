import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import subprocess
import threading
import sys
import os

class YTDLPGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("yt-dlp GUI")
        self.root.geometry("700x400")

        # YouTube URL input
        tk.Label(self.root, text="YouTube URL:").place(x=10, y=10)
        self.url = tk.Entry(self.root, width=83)
        self.url.place(x=10, y=40)

        # Audio format input
        tk.Label(self.root, text="Audio format:").place(x=10, y=80)
        self.audio_format = ttk.Combobox(self.root, values=["best", "aac", "flac", "mp3", "m4a", "opus", "vorbis", "wav"], width=10)
        self.audio_format.place(x=110, y=80)
        self.audio_format.current(0)

        # Video format input
        tk.Label(self.root, text="Video format:").place(x=250, y=80)
        self.video_format = ttk.Combobox(self.root, values=["none", "best", "mp4", "webm", "avi", "mkv", "flv"], width=10)
        self.video_format.place(x=350, y=80)
        self.video_format.current(0)

        # PLaylist checkbox
        tk.Label(self.root, text="Playlist:").place(x=480, y=80)
        self.playlist = tk.BooleanVar()
        self.playlist.set(False)
        tk.Checkbutton(self.root, variable=self.playlist).place(x=530, y=80)

        # Submit button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.place(x=580, y=75)

        # Status box
        self.status = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=83, height=14)
        self.status.place(x=10, y=120)

        self.root.mainloop()

    def submit(self):
        """Handles the submit button click."""
        url = self.url.get()
        audio_format = self.audio_format.get()
        self.status.insert(tk.END, f"Downloading: {url} in {audio_format} format\n")
        self.status.see(tk.END)

if sys.platform == "win32":
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")

YTDLPGui()
