from pytube import YouTube

import os


"""
Downloads a Youtube video to VIDEO_PATH.
"""
def download_yt(url: str, path: str) -> None:
    try:
        YouTube(url).streams.get_highest_resolution().download(filename=path)
    except:
        print("Failed to download video")
        exit(1)


"""
Returns width and height of the terminal this program is run in.
"""
def get_terminal_dimensions() -> tuple[int, int]:
    size = os.get_terminal_size()
    return size.columns, size.lines


"""
Fast ceiling division
"""
def ceil_div(n, d):
    return -(n // -d)
