from ffmpeg_progress_yield import FfmpegProgress
from tqdm import tqdm

import ffmpeg
import shlex
import math
import os

from utils.files import *
from utils.other import *

SCALE_FACTOR = 0.45  # Terminal characters are taller than they are wide


"""
Handles rescaling and frame splitting of videos.
"""
class FrameDownloader:
    def __init__(self, width: int | None, video_path: str, frames_dir: str, fps: int | None) -> None:
        self.width = width
        self.height = 0
        self.frames_dir = frames_dir
        self.video_path = video_path
        self.fps = fps


    def get_fps(self) -> int:
        return self.fps


    """
    Checks a bunch of conditions to see if the frames for a video already exist. Uses prev.txt to cache the
    parameters of the previous execution.
    """
    def fetch_frames(self, url: str) -> None:
        if os.path.isfile(self.video_path):  # set_resolution() needs the mp4 file
            self.set_resolution()
        else:
            remove_dir(self.frames_dir)

        if not os.path.isfile('prev.txt'):
            remove_dir(self.frames_dir)
        else:
            prev_w, prev_url, prev_fps = open('prev.txt', 'r').read().split('\n')

            if prev_w == 'None' or prev_fps == 'None':
                prev_w = prev_fps = None
            else:
                prev_w, prev_fps = int(prev_w), int(prev_fps)

            if prev_w != self.width or prev_url != url or prev_fps != self.fps:
                remove_dir(self.frames_dir)

        if not os.path.exists(self.frames_dir) or len(os.listdir(self.frames_dir)) == 0:
            os.mkdir(self.frames_dir)
            self._split_frames()

        with open('prev.txt', 'w') as f:
            f.write('\n'.join((str(self.width), url, str(self.fps))))


    """
    Sets the width, height, and FPS depending on if they were provided in command line args.
    """
    def set_resolution(self) -> None:
        if self.fps is None:  # Was not provided by cmd line
            video_info = ffmpeg.probe(self.video_path, select_streams = "v")['streams'][0]
            avg_fps = video_info['avg_frame_rate'].split('/')
            self.fps = int(avg_fps[0]) // int(avg_fps[1])

        if self.width is None:  # Was not provided by cmd line
            t_width, t_height = get_terminal_dimensions()
            r = t_height / t_width
            self.width = t_width
            self.height = math.floor(self.width * r) - 2  # space for progress bar
        else:
            video_info = ffmpeg.probe(self.video_path, select_streams = "v")['streams'][0]
            ratio = video_info['display_aspect_ratio'].split(':')
            r = int(ratio[1]) / int(ratio[0])
            self.height = int(self.width * r * SCALE_FACTOR) - 2


    """
    Calls FFmpeg to rescale the image and split the video at a given framerate. Progress bar is used
    to visualize current status.
    """
    def _split_frames(self) -> None:
        ff = FfmpegProgress(shlex.split(f'ffmpeg -i {self.video_path} -vf "fps={self.fps},scale={self.width}:{self.height}" {self.frames_dir}/%05d.png'))

        with tqdm(total=100, desc="Extracting frames", unit='%', colour='WHITE') as pbar:
            for progress in ff.run_command_with_progress():
                pbar.update(progress - pbar.n)
