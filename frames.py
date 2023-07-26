from PIL import Image
from pytube import YouTube
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

import subprocess
import shutil
import shlex
import os
import re


WORKERS = None
CHUNK_SIZE = 4

SCALE_FACTOR = 0.45

RESET_CODE = '\033c'
       

def remove_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)


class FrameDownloader:
    def __init__(self, width, frames_dir, pixel_frames_dir):
        self.width = width
        self.height = 0
        self.frames_dir = frames_dir
        self.pixel_frames_dir = pixel_frames_dir


    def fetch_frames(self, url):
        if not os.path.isfile('prev.txt'):
            remove_dir(self.frames_dir)
            remove_dir(self.pixel_frames_dir)
        else:
            prev_w, prev_url = open('prev.txt', 'r').readlines()
            if prev_url != url:
                remove_dir(self.frames_dir)
                remove_dir(self.pixel_frames_dir)

            if int(prev_w) != self.width:
                remove_dir(self.pixel_frames_dir)

        if (not os.path.exists(self.frames_dir)):
            os.mkdir(self.frames_dir)
            self._download_yt(url)
            self._split_frames()

        if (not os.path.exists(self.pixel_frames_dir)):
            os.mkdir(self.pixel_frames_dir)
            self._pixelate_all_frames()

        with open('prev.txt', 'w') as f:
            f.write('\n'.join([str(self.width), url]))


    def _download_yt(self, url):
        video = YouTube(url)
        video = video.streams.get_highest_resolution()

        try:
            video.download(filename='video.mp4')
        except:
            print("Failed to download video\n")
            exit(1)


    def _split_frames(self):
        subprocess.run(shlex.split(f"ffmpeg -i ./video.mp4 '{self.frames_dir}/%05d.png'"))
    

    # 'with' blocks until all the files are resized
    def _pixelate_all_frames(self):
        with ProcessPoolExecutor(max_workers=WORKERS) as executor:
            files = [os.path.join(self.frames_dir, f) for f in os.listdir(self.frames_dir)]
            sorted_files = sorted(files, key=lambda x: int(re.sub('[^0-9]', '', x)))
            for _ in tqdm(executor.map(self._pixelate_frame, enumerate(sorted_files), chunksize=CHUNK_SIZE), 
                          total=len(sorted_files),
                          desc='Resizing video frames'):
                pass


    def _pixelate_frame(self, pair):
        img = Image.open(pair[1])

        if self.height == 0: 
            orig_width, orig_height = img.size
            r = orig_height / orig_width
            self.height = int(self.width * r * SCALE_FACTOR)

        resized_img = img.resize((self.width, self.height), Image.LANCZOS)
        resized_img.save(f'{self.pixel_frames_dir}/{pair[0]}.png')
