import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import ttk
import subprocess
import threading
import sys
import os

class YTDLPGui:
    def __init__(self):
        root = tk.Tk()
        root.title("yt-dlp GUI")
        root.geometry("700x400")

        # YouTube URL input
        tk.Label(root, text="YouTube URL:").place(x=10, y=10)
        self.url = tk.Entry(root, width=83)
        self.url.place(x=10, y=40)

        # Audio format input
        tk.Label(root, text="Audio format:").place(x=10, y=80)
        self.audio_format = ttk.Combobox(root, values=["best", "aac", "flac", "mp3", "m4a", "opus", "vorbis", "wav"], width=10)
        self.audio_format.place(x=110, y=80)
        self.audio_format.current(0)

        # Video format input
        tk.Label(root, text="Video format:").place(x=10, y=120)
        self.video_format = ttk.Combobox(root, values=["none", "best", "mp4", "webm", "avi", "mkv", "flv"], width=10)
        self.video_format.place(x=110, y=120)
        self.video_format.current(0)
        self.video_format.bind("<<ComboboxSelected>>", lambda event: self.update_audio_combobox_state())

        # PLaylist checkbox
        tk.Label(root, text="Playlist:").place(x=265, y=120)
        self.playlist = tk.BooleanVar()
        self.playlist.set(False)
        tk.Checkbutton(root, variable=self.playlist).place(x=315, y=120)

        # Submit button
        submit_button = tk.Button(root, text="Submit", command=self.submit)
        submit_button.place(x=605, y=115)

        # Output location button
        change_dir = tk.Button(root, text="Change Output Directory", command=self.select_dir)
        change_dir.place(x=400, y=115)

        # Current directory
        tk.Label(root, text="Current Directory:").place(x=265, y=80)
        self.current_dir = tk.Entry(root, width=34)
        self.current_dir.place(x=400, y=80)
        self.current_dir.insert(0, os.getcwd())
        self.current_dir["state"] = "readonly"

        # Status box
        self.status = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=83, height=12)
        self.status.place(x=10, y=160)

        root.mainloop()

    def submit(self):
        """Handles the submit button click."""
        url = self.url.get()
        self.url.delete(0, tk.END)

        audio_format = self.audio_format.get()
        video_format = self.video_format.get()
        playlist = self.playlist.get()
        self.log(f"==> Downloading: {url}\n==> Video: {video_format}\n==> Audio: {audio_format}\n==> Playlist: {playlist}\n")

        command = "yt-dlp -f" # Starts building the yt-dlp command
        if video_format != "none":
            command += " bestvideo+bestaudio"
            if video_format != "best":
                command += f" --recode-video {video_format}"
        else:
            command += " bestaudio"
            if audio_format != "best":
                command += f" --extract-audio --audio-format {audio_format}"
        if not playlist:
            command += " --no-playlist"
        command += f" -o \"{self.current_dir.get()}/%(title)s.%(ext)s\" {url}"

        self.log(f"=>$ {command}\n")
        process = threading.Thread(target=self.yt_dlp, args=(command,))
        process.daemon = True
        process.start()

    def yt_dlp(self, command):
        """Runs the yt-dlp command."""
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                self.log(output)
        process.stdout.close()
        self.log("\n==> Download complete!\n")

    def select_dir(self):
        """Opens a file dialog to select the output location."""
        output_dir = filedialog.askdirectory()
        if output_dir:
            os.chdir(output_dir)
            self.current_dir["state"] = "normal"
            self.current_dir.delete(0, tk.END)
            self.current_dir.insert(0, output_dir)
            self.current_dir["state"] = "readonly"
            self.log(f"==> Output location: {output_dir}\n")

    def update_audio_combobox_state(self):
        """Grays out the audio combobox if the video format is not none."""
        if self.video_format.get() == "none":
            self.audio_format["state"] = "normal"
        else:
            self.audio_format["state"] = "disabled"

    def log(self, message):
        """Logs a message to the status box."""
        self.status.insert(tk.END, message)
        self.status.see(tk.END)

if sys.platform == "win32":
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")

YTDLPGui()
