import asyncio
import threading
import tkinter as tk
from tkinter import ttk, filedialog

import settings
from ffmpeg_funcs import *


class FFmpegVolumeTrimGUI:
    def __init__(self, window_size: tuple[int, int], window_title: str, resizable: tuple[bool, bool] = (False, False)):
        self.window_size = window_size
        self.resizable = resizable
        self._hyphen_label, self._time_label, self._trim_end_entry, self._trim_start_entry, \
            self._volume_entry, self._volume_slider, self._volume, self._file, self._file_label, self._trim_image, \
            self._audio_image, self._download_image = None, None, None, None, None, None, None, None, None, None, \
            None, None

        # initialize the window
        self.root = tk.Tk()
        self.root.title(window_title)
        self.root.resizable(self.resizable[0], self.resizable[1])
        self.root.iconbitmap(settings.ICON_IMAGE_PATH)

        # window sizing
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (window_size[0] / 2))
        y = int((screen_height / 2) - (window_size[1] / 2))
        self.root.geometry(f"{window_size[0]}x{window_size[1]}+{x}+{y}")

        # ask file button
        self._folder_image = tk.PhotoImage(file=settings.FOLDER_IMAGE_PATH).subsample(
                settings.FOLDER_IMAGE_SUBSAMPLE[0],
                settings.FOLDER_IMAGE_SUBSAMPLE[1])
        ask_file_button = ttk.Button(self.root, text="Choose a file", image=self._folder_image,
                                     compound="left", command=self.open_file)
        ask_file_button.place(relx=0.5, rely=0.1, anchor="center")

        # Initialize result label beside download button
        self.result_label = ttk.Label(self.root, text="")

    def open_file(self):
        """Method for asking for a filepath and opening it using tkinter, used for the 'Choose a file' tkinter
        button.
        """
        self._file = filedialog.askopenfilename(filetypes=[("Audio/Video Files", ".mp3 .wav .mp4")])
        if not self._file:
            return
        max_chars = 40
        label_text = self._file.split("/")[-1]
        if len(label_text) > max_chars:  # cut off the file name if it is too long
            label_text = f"{label_text[:max_chars - 4]}...{label_text.split('.')[-1]}"
        try:
            self._file_label.configure(text=label_text)
        except AttributeError:
            self._file_label = ttk.Label(self.root, text=label_text)
            self._file_label.place(relx=0.5, rely=0.25, anchor="center")

        # Create the Volume and Trim buttons
        self.create_volume_button()
        self.create_trim_button()

    def create_volume_button(self) -> None:
        """Creates the volume button widget. The button creates the volume slider and download button widgets."""
        self._audio_image = tk.PhotoImage(file=settings.AUDIO_IMAGE_PATH).subsample(
                settings.AUDIO_IMAGE_SUBSAMPLE[0],
                settings.AUDIO_IMAGE_SUBSAMPLE[1])
        volume_button = ttk.Button(self.root, text="Volume", image=self._audio_image,
                                   compound="left", command=self.create_volume_slider)
        volume_button.place(relx=0.3, rely=0.4, anchor="center")

    def create_trim_button(self) -> None:
        """Creates the trim button widget. The button creates the trim entry and save button widgets."""
        self._trim_image = tk.PhotoImage(file=settings.TRIM_IMAGE_PATH).subsample(
                settings.TRIM_IMAGE_SUBSAMPLE[0],
                settings.TRIM_IMAGE_SUBSAMPLE[1])
        trim_button = ttk.Button(self.root, text="Trim", image=self._trim_image,
                                 compound="left", command=self.create_trim_entries)
        trim_button.place(relx=0.7, rely=0.4, anchor="center")

    def create_volume_slider(self) -> None:
        """Creates the volume slider widget."""
        # remove the trim entry widgets if they exist:
        self.hide_trim_entries()

        self._volume = tk.IntVar()
        self._volume.set(100)
        volume_str = tk.StringVar()
        volume_str.set("100%")

        def on_volume_change(event) -> None:
            volume_str.set(f"{self._volume.get()}%")

        self._volume_slider = ttk.Scale(self.root, from_=0, to=1000, orient="horizontal",
                                        length=200, variable=self._volume, command=on_volume_change)
        self._volume_entry = ttk.Entry(self.root, textvariable=volume_str, width=6, justify="center")

        def on_entry_change(event) -> None:
            if "%" not in (value := volume_str.get()):
                self._volume_slider.set(int(value))
                self._volume.set(int(value))
            else:
                self._volume_slider.set(int(value[:-1]))
                self._volume.set(int(value[:-1]))

        # when the user presses enter the slider changes to the given value:
        self._volume_entry.bind("<Return>", on_entry_change)

        slider_position = (0.5, 0.58)
        self._volume_slider.place(relx=slider_position[0], rely=slider_position[1], anchor="center")
        self._volume_entry.place(relx=slider_position[0], rely=slider_position[1] + 0.145, anchor="center")

        self.create_save_button("volume")

    def create_trim_entries(self) -> None:
        self.hide_volume_slider()  # hide the volume slider if it exists

        # Start and end time entries
        entry_width = 7
        start_var = tk.StringVar()

        self._trim_start_entry = ttk.Entry(self.root, textvariable=start_var, width=entry_width)
        end_var = tk.StringVar()
        self._trim_end_entry = ttk.Entry(self.root, textvariable=end_var, width=entry_width)

        # Labels
        self._trim_label = ttk.Label(self.root, text="Start - end:")
        self._time_label = ttk.Label(self.root, text="(hh:mm:ss)")
        self._hyphen_label = ttk.Label(self.root, text="-")

        # Placement
        x, y = 0.5, 0.6
        xpad = 0.13
        ypad = 0.1
        self._trim_label.place(relx=xpad, rely=y, anchor="center")
        self._trim_start_entry.place(relx=x - xpad, rely=y, anchor="center")
        self._trim_end_entry.place(relx=x + xpad, rely=y, anchor="center")
        self._time_label.place(relx=xpad, rely=y+ypad, anchor="center")
        self._hyphen_label.place(relx=x, rely=y, anchor="center")

        self.create_save_button("trim")

    def hide_volume_slider(self) -> None:
        """Hides the volume slider widget if they exist."""
        try:
            self._volume_slider.place_forget()
            self._volume_entry.place_forget()
        except AttributeError:
            return

    def hide_trim_entries(self) -> None:
        """Hide both trim entry widgets if they exist."""
        try:
            self._trim_start_entry.place_forget()
            self._trim_end_entry.place_forget()
            self._trim_label.place_forget()
            self._time_label.place_forget()
            self._hyphen_label.place_forget()
        except AttributeError:
            return

    def create_save_button(self, click_type: str) -> None:
        """Creates the save button widget."""
        x, y = 0.5, 0.9

        async def async_saving_message() -> None:
            self.result_label.configure(text="Saving...")

        def download() -> None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            output_file = None
            match click_type:
                case "volume":
                    output_file = ffmpeg_volume(self._file, self._volume.get() / 100)
                case "trim":
                    start = self._trim_start_entry.get()
                    end = self._trim_end_entry.get()
                    output_file = ffmpeg_trim(self._file, start, end)

            async def download_task():
                await async_saving_message()
                self.result_label.place(relx=x + 0.335, rely=y, anchor="center")
                output_file.run(overwrite_output=True)

            def start_download():
                loop.run_until_complete(download_task())
                loop.close()
                self.result_label.configure(text="Done!")

            threading.Thread(target=start_download).start()

        self._download_image = tk.PhotoImage(file=settings.DOWNLOAD_IMAGE_PATH).subsample(
                settings.DOWNLOAD_IMAGE_SUBSAMPLE[0],
                settings.DOWNLOAD_IMAGE_SUBSAMPLE[1])
        download_button = ttk.Button(self.root, text="Save", image=self._download_image,
                                     compound="left", command=download)
        download_button.place(relx=x, rely=y, anchor="center")

    def run(self):
        """Runs the GUI."""
        self.root.mainloop()
