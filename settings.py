import os
import sys


def get_absolute_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


WINDOW_SIZE = (290, 210)
WINDOW_TITLE = "Volumer & Trimmer"

FOLDER_IMAGE_PATH = get_absolute_path(r"data\folder.png")
FOLDER_IMAGE_SUBSAMPLE = (30, 30)
DOWNLOAD_IMAGE_PATH = get_absolute_path(r"data\download.png")
DOWNLOAD_IMAGE_SUBSAMPLE = FOLDER_IMAGE_SUBSAMPLE
AUDIO_IMAGE_PATH = get_absolute_path(r"data\audio.png")
AUDIO_IMAGE_SUBSAMPLE = FOLDER_IMAGE_SUBSAMPLE
TRIM_IMAGE_PATH = get_absolute_path(r"data\trim.png")
TRIM_IMAGE_SUBSAMPLE = FOLDER_IMAGE_SUBSAMPLE
ICON_IMAGE_PATH = get_absolute_path(r"data\icon.ico")
