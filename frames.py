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


class FrameDownloader:
    def __init__(self, width, video_path, frames_dir, fps):
        self.width = width
        self.height = 0
        self.frames_dir = frames_dir
        self.video_path = video_path
        self.fps = fps


    def fetch_frames(self, url):
        if not os.path.isfile('prev.txt'):
            remove_dir(self.frames_dir)
            print('belh')
        else:
            prev_w, prev_url, prev_fps = open('prev.txt', 'r').read().split('\n')
            if int(prev_w) != self.width or prev_url != url or int(prev_fps) != self.fps:
                remove_dir(self.frames_dir)

        if not os.path.exists(self.frames_dir):
            os.mkdir(self.frames_dir)
            self._split_frames()

        with open('prev.txt', 'w') as f:
            f.write('\n'.join((str(self.width), url, str(self.fps))))


    def _split_frames(self):
        video_info = ffmpeg.probe(self.video_path, select_streams = "v")['streams'][0]

        ratio = video_info['display_aspect_ratio'].split(':')
        r = float(ratio[1]) / float(ratio[0])
        self.height = int(self.width * r * SCALE_FACTOR)

        ff = FfmpegProgress(shlex.split(f'ffmpeg -i {self.video_path} -vf "fps={self.fps},scale={self.width}:{self.height}" {self.frames_dir}/%05d.png'))
        with tqdm(total=100, desc="Extracting frames", unit='%', colour='WHITE') as pbar:
            for progress in ff.run_command_with_progress():
                pbar.update(progress - pbar.n)
