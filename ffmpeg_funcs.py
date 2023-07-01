import ffmpeg


def ffmpeg_volume(file: str, volume: float | int, outfile: str = None) -> ffmpeg.nodes.OutputStream:
    """Changes the volume of the file using ffmpeg."""
    if volume < 0:
        raise ValueError("New volume must be a non-negative number.")
    if outfile is None:
        file_ext = file.split(".")[-1]
        out_file = file.replace(f".{file_ext}", f"_volumeboost_{volume}.{file_ext}")
    return (
        ffmpeg
        .input(file)
        .filter("volume", volume)
        .output(out_file, loglevel="quiet")
    )


def ffmpeg_trim(file: str, start: str, end: str, outfile: str = None) -> ffmpeg.nodes.OutputStream:
    """Trims the file using ffmpeg."""
    start = format_time_string(start)
    end = format_time_string(end)
    if start >= end:
        raise ValueError("Start time must be before end time.")
    file_ext = file.split(".")[-1]
    if outfile is None:
        out_file = file.replace(f".{file_ext}", f"_trimmed.{file_ext}")
    match file_ext:
        case "mp3" | "wav":
            return (
                ffmpeg
                .input(file)
                .filter_('atrim', start=start, end=end)
                .filter_('asetpts', 'PTS-STARTPTS')
                .output(out_file, loglevel="quiet")
            )
        case "mp4" | "mkv":
            vid = (
                ffmpeg
                .input(file)
                .trim(start=start, end=end)
                .setpts('PTS-STARTPTS')
            )
            aud = (
                ffmpeg
                .input(file)
                .filter_('atrim', start=start, end=end)
                .filter_('asetpts', 'PTS-STARTPTS')
            )

            joined = ffmpeg.concat(vid, aud, v=1, a=1).node
            return ffmpeg.output(joined[0], joined[1], out_file, loglevel="quiet")
        case _:
            raise NameError("File must be a mp3, wav, mp4, or mkv file.")


def format_time_string(time: str):
    if len(time) == 1:
        time = "0" + time
    if 5 <= len(time) < 8:  # only given minute and seconds
        return "00:" + time
    elif len(time) < 5:  # only given seconds
        return "00:00:" + time
