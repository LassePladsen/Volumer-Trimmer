import settings
from VolumeTrimGUI import FFmpegVolumeTrimGUI

if __name__ == "__main__":
    window = FFmpegVolumeTrimGUI(window_size=settings.WINDOW_SIZE, window_title=settings.WINDOW_TITLE)
    window.run()
