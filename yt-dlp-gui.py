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
        # Add ffmpeg to the PATH
        self.env = os.environ.copy()
        self.env['PATH'] = self.get_ffmpeg_path() + os.pathsep + self.env['PATH']

        # Create the GUI
        root = tk.Tk()
        root.title("yt-dlp GUI")
        root.geometry("800x500")

        style = ttk.Style()
        style.theme_use("clam")

        # Set the grid layout
        root.grid_rowconfigure(0, weight=1, minsize=55)
        root.grid_rowconfigure(1, weight=1, minsize=55)
        root.grid_rowconfigure(2, weight=1, minsize=55)
        root.grid_rowconfigure(3, weight=15, minsize=100)

        root.grid_columnconfigure(1, weight=1, minsize=80)
        root.grid_columnconfigure(4, weight=5, minsize=200)
        root.grid_columnconfigure(5, weight=5, minsize=100)

        # YouTube URL input
        ttk.Label(root, text="YouTube URL:").grid(column=0, row=0, padx=10, pady=10)
        self.url = ttk.Entry(root)
        self.url.grid(column=1, row=0, columnspan=5, sticky="nsew", padx=10, pady=10)

        # Audio format input
        ttk.Label(root, text="Audio format:").grid(column=0, row=1, padx=10, pady=10)
        self.audio_format = ttk.Combobox(root, values=["best", "aac", "flac", "mp3", "m4a", "opus", "vorbis", "wav"], width=10)
        self.audio_format.grid(column=1, row=1, sticky="nsew", padx=10, pady=10)
        self.audio_format.current(0)
        self.audio_format.bind("<<ComboboxSelected>>", lambda event: self.audio_format.select_clear())

        # Video format input
        ttk.Label(root, text="Video format:").grid(column=0, row=2, padx=10, pady=10)
        self.video_format = ttk.Combobox(root, values=["---", "best", "mp4", "webm", "avi", "mkv", "flv"], width=10)
        self.video_format.grid(column=1, row=2, sticky="nsew", padx=10, pady=10)
        self.video_format.current(0)
        self.video_format.bind("<<ComboboxSelected>>", lambda event: self.update_audio_combobox_state())

        # PLaylist checkbox
        ttk.Label(root, text="Playlist:").grid(column=2, row=2, padx=10, pady=10)
        self.playlist = tk.BooleanVar()
        self.playlist.set(False)
        ttk.Checkbutton(root, variable=self.playlist).grid(column=3, row=2, padx=10, pady=10)

        # Submit button
        submit_button = ttk.Button(root, text="Submit", command=self.submit)
        submit_button.grid(column=5, row=2, sticky="nsew", padx=10, pady=10)

        # Output location button
        change_dir = ttk.Button(root, text="Change Output Directory", command=self.select_dir)
        change_dir.grid(column=4, row=2, sticky="nsew", padx=10, pady=10)

        # Current directory
        ttk.Label(root, text="Current Directory:").grid(column=2, row=1, padx=10, pady=10)
        self.current_dir = ttk.Entry(root)
        self.current_dir.grid(column=3, row=1, columnspan=3, sticky="nswe", padx=10, pady=10)
        self.current_dir.insert(0, os.getcwd())
        self.current_dir["state"] = "readonly"

        # Status box
        self.status = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.status.grid(column=0, row=3, columnspan=6, sticky="nsew", padx=10, pady=10)
        self.status["state"] = "disabled"

        self.welcome()

        root.mainloop()

    def submit(self):
        """Handles the submit button click."""
        url = self.url.get()
        self.url.delete(0, tk.END)

        audio_format = self.audio_format.get()
        video_format = self.video_format.get()
        playlist = self.playlist.get()
        self.log(f"==> Downloading: {url}\n==> Video: {video_format}\n==> Audio: {audio_format}\n==> Playlist: {playlist}\n")

        command = f"{self.get_yt_dlp_path()}"
        if video_format != "---":
            command += " -f bestvideo+bestaudio"
            if video_format != "best":
                command += f" --recode-video {video_format}"
        else:
            command += " -x -f bestaudio"
            if audio_format != "best":
                command += f" --audio-format {audio_format}"
        if not playlist:
            command += " --no-playlist"
        else:
            command += " --yes-playlist"
        command += f" -o \"{self.current_dir.get()}{os.sep}%(title)s.%(ext)s\" \"{url}\""

        self.log(f"=>$ {command}\n")
        process = threading.Thread(target=self.yt_dlp, args=(command,))
        process.daemon = True
        process.start()

    def yt_dlp(self, command):
        """Runs the yt-dlp command."""
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, env=self.env)
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
            self.current_dir["state"] = "normal"
            self.current_dir.delete(0, tk.END)
            self.current_dir.insert(0, output_dir)
            self.current_dir["state"] = "readonly"
            self.log(f"==> Output location: {output_dir}\n")

    def update_audio_combobox_state(self):
        """Grays out the audio combobox if the video format is not ---."""
        if self.video_format.get() == "---":
            self.audio_format["state"] = "normal"
            self.audio_format.current(0)
        else:
            self.audio_format.set("---")
            self.audio_format["state"] = "disabled"
        self.video_format.select_clear()

    def log(self, message):
        """Logs a message to the status box."""
        self.status["state"] = "normal"
        self.status.insert(tk.END, message)
        self.status.see(tk.END)
        self.status["state"] = "disabled"

    def get_ffmpeg_path(self):
        """Returns the path to the ffmpeg binary."""
        if getattr(sys, 'frozen', False):
            return os.path.join(sys._MEIPASS, "ffmpeg")
        else:
            return "ffmpeg" if sys.platform == "linux" else "ffmpeg.exe"

    def get_yt_dlp_path(self):
        """Returns the path to the yt-dlp binary."""
        if getattr(sys, 'frozen', False):
            return os.path.join(sys._MEIPASS, "yt-dlp")
        else:
            return "yt-dlp" if sys.platform == "linux" else "yt-dlp.exe"

    def welcome(self):
        """Prints basic instructions to status box."""
        self.log("                       __            ____         ________  ______\n")
        self.log("                __  __/ /_      ____/ / /___     / ____/ / / /  _/\n")
        self.log("               / / / / __/_____/ __  / / __ \\   / / __/ / / // /  \n")
        self.log("              / /_/ / /_/_____/ /_/ / / /_/ /  / /_/ / /_/ // /   \n")
        self.log("              \\__, /\\__/      \\__,_/_/ .___/   \\____/\\____/___/   \n")
        self.log("             /____/                 /_/                           \n")
        self.log("\n==|    Options\n")
        self.log("==|    __best__                   |    Best quality, fastest download\n")
        self.log("==|    __other_predefined__       |    Incurs additional processing time\n")
        self.log("==|    __other_not_predefined__   |    Manual dropdown field override possible\n")

if sys.platform == "win32":
    """Suppresses the console window on Windows."""
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")

YTDLPGui()
