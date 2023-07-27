from ffmpeg_progress_yield import FfmpegProgress
from tqdm import tqdm

import ffmpeg
import shutil
import shlex
import os


WORKERS = None
CHUNK_SIZE = 4

SCALE_FACTOR = 0.45


def remove_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)


def get_terminal_width():
    size = os.get_terminal_size()
    return size.columns, size.lines


class FrameDownloader:
    def __init__(self, width, video_path, frames_dir, fps):
        self.width = width
        self.height = 0
        self.frames_dir = frames_dir
        self.video_path = video_path
        self.fps = fps


    def get_width(self):
        return self.width


    def get_fps(self):
        return self.fps


    def fetch_frames(self, url):
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

        if not os.path.exists(self.frames_dir):
            os.mkdir(self.frames_dir)
            self._split_frames()

        with open('prev.txt', 'w') as f:
            f.write('\n'.join((str(self.width), url, str(self.fps))))


    def _split_frames(self):
        if self.fps is None:
            video_info = ffmpeg.probe(self.video_path, select_streams = "v")['streams'][0]
            avg_fps = video_info['avg_frame_rate'].split('/')
            self.fps = int(avg_fps[0]) // int(avg_fps[1])

        if self.width is None:
            self.width, t_height = get_terminal_width()
            r = t_height / self.width
            self.height = int(self.width * r) - 2
        else:
            video_info = ffmpeg.probe(self.video_path, select_streams = "v")['streams'][0]
            ratio = video_info['display_aspect_ratio'].split(':')
            r = int(ratio[1]) / int(ratio[0])
            self.height = int(self.width * r * SCALE_FACTOR)

        ff = FfmpegProgress(shlex.split(f'ffmpeg -i {self.video_path} -vf "fps={self.fps},scale={self.width}:{self.height}" {self.frames_dir}/%05d.png'))
        with tqdm(total=100, desc="Extracting frames", unit='%', colour='WHITE') as pbar:
            for progress in ff.run_command_with_progress():
                pbar.update(progress - pbar.n)
