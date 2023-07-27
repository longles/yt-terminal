from argparse import ArgumentParser
from terminal import Renderer
from frames import FrameDownloader
from pytube import YouTube


VIDEO_PATH = './video.mp4'
FRAMES_DIR = './frames'

WORKERS = None  # Automatically decide number of processes to spawn
CHUNK_SIZE = 4


"""
Download a Youtube video to VIDEO_PATH.
"""
def download_yt(url: str) -> None:
    try:
        YouTube(url).streams.get_highest_resolution().download(filename=VIDEO_PATH)
    except:
        print("Failed to download video")
        exit(1)


"""
Checks if the resolution and fps provided command line args are valid.
"""
def validate_input(resolution: str | None, fps: str | None) -> tuple[int | None, int | None]:
    def check_resolution(resolution):
        try:
            r = int(resolution)
            if r < 4:
                print('Choose a higher resolution!')
                exit(1)
            return r
        except ValueError:
            print('Resolution is invalid!')
            exit(1)

    def check_fps(fps):
        try:
            f = int(fps)
            if f < 1:
                print('Choose a higher fps!')
                exit(1)
            return f
        except ValueError:
            print('FPS is invalid!')
            exit(1)

    if resolution is None and fps is None:
        return resolution, fps

    if resolution is None:
        return resolution, check_fps(fps)

    if fps is None:
        return check_resolution(resolution), fps

    return check_resolution(r), check_fps(fps)


if __name__ == '__main__':
    parser = ArgumentParser(description='Convert youtube videos into terminal animations')
    parser.add_argument('-r', '--resolution', default=None)
    parser.add_argument('-f', '--fps', default=None)
    parser.add_argument('-u', '--url', required=True)

    args = vars(parser.parse_args())

    r = args['resolution']
    f = args['fps']
    url = args['url']

    resolution, fps = validate_input(r, f)

    download_yt(url)

    frame = FrameDownloader(resolution, VIDEO_PATH, FRAMES_DIR, fps)
    frame.fetch_frames(url)

    term = Renderer(frame.get_width(), FRAMES_DIR, frame.get_fps(), WORKERS, CHUNK_SIZE)
    term.render()
