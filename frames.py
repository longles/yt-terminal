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

RESET_CODE = '\033c'
       

class FrameDownloader:
    def __init__(self, width, height, frame_dir, pixel_frames_dir):
        self.width = width
        self.height = height
        self.frame_dir = frame_dir
        self.pixel_frames_dir = pixel_frames_dir


    def fetch_frames(self, url):
        if not os.path.isfile('prev.txt'):
            if os.path.exists(self.frame_dir) and os.path.exists(self.pixel_frames_dir):
                shutil.rmtree(self.frame_dir)
                shutil.rmtree(self.pixel_frames_dir)
        else:
            prev_w, prev_h, prev_url = open('prev.txt', 'r').readlines()
            if prev_url != url:
                shutil.rmtree(self.frame_dir)
            if int(prev_w) != self.width or int(prev_h) != self.height:
                shutil.rmtree(self.pixel_frames_dir)

        if (not os.path.exists(self.frame_dir)):
            os.mkdir(self.frame_dir)
            self._download_yt(url)
            self._split_frames()

        if (not os.path.exists(self.pixel_frames_dir)):
            os.mkdir(self.pixel_frames_dir)
            self._pixelate_all_frames()
        
        with open('prev.txt', 'w') as f:
            f.write('\n'.join([str(self.width), str(self.height), url]))


    def _download_yt(self, url):
        video = YouTube(url)
        video = video.streams.get_highest_resolution()

        try:
            video.download(filename='video.mp4')
        except:
            print("Failed to download video\n")
            exit(1)


    def _split_frames(self):
        subprocess.run(shlex.split(f"ffmpeg -i ./video.mp4 '{self.frame_dir}/%05d.png'"))
    

    # 'with' blocks until all the files are resized
    def _pixelate_all_frames(self):
        with ProcessPoolExecutor(max_workers=WORKERS) as executor:
            files = [os.path.join(self.frame_dir, f) for f in os.listdir(self.frame_dir)]
            sorted_files = sorted(files, key=lambda x: int(re.sub('[^0-9]', '', x)))
            for _ in tqdm(executor.map(self._pixelate_frame, enumerate(sorted_files), chunksize=CHUNK_SIZE), 
                          total=len(sorted_files),
                          desc='Resizing video frames'):
                pass
            
            # print(RESET_CODE)


    def _pixelate_all_frames_seq(self):
        files = [os.path.join(self.frame_dir, f) for f in os.listdir(self.frame_dir)]
        sorted_files = sorted(files, key=lambda x: int(re.sub('[^0-9]', '', x)))
        for x in tqdm(enumerate(sorted_files),
                        total=len(sorted_files),
                        desc='Resizing video frames'):
            self._pixelate_frame(x)
        
        print(RESET_CODE)


    def _pixelate_frame(self, pair):
        img = Image.open(pair[1])
        resized_img = img.resize((self.width, self.height), Image.BILINEAR)
        resized_img.save(f'{self.pixel_frames_dir}/{pair[0]}.png')
