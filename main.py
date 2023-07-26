from argparse import ArgumentParser
from terminal import Renderer
from frames import FrameDownloader
from pytube import YouTube

import ffmpeg


VIDEO_PATH = './video.mp4'
FRAMES_DIR = './frames'


def download_yt(url):
    try:
        YouTube(url).streams.get_highest_resolution().download(filename='video.mp4')
    except:
        print("Failed to download video")
        exit(1)


if __name__ == '__main__':
    parser = ArgumentParser(description='Convert youtube videos into terminal animations')
    parser.add_argument('-r', '--resolution', required=True)
    parser.add_argument('-u', '--url',required=True)
    parser.add_argument('-f', '--fps', default=None)

    args = vars(parser.parse_args())

    resolution = int(args['resolution'])
    fps = args['fps']
    url = args['url']

    download_yt(url)

    if fps is None:
        video_info = ffmpeg.probe(VIDEO_PATH, select_streams = "v")['streams'][0]
        avg_fps = video_info['avg_frame_rate'].split('/')
        fps = int(avg_fps[0]) // int(avg_fps[1])
    else:
        fps = int(fps)

    frame = FrameDownloader(resolution, VIDEO_PATH, FRAMES_DIR, fps)
    term = Renderer(resolution, FRAMES_DIR, fps)

    frame.fetch_frames(url)
    term.render()
