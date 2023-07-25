from PIL import Image
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

import numpy as np
import time
import os
import re

FPS = 30
WORKERS = None
CHUNK_SIZE = 4

END_CODE = '\033[0;0m'
CLEAR_CODE = '\033[2J'
REFRESH_CODE = '\033[H'
RESET_CODE = '\033c'

TILE = '█'
BLACK = 0


def fg_code(rgb):
    return f'\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m'


def bg_code(color):
    return f'\033[48;5;{color}m'


class Renderer:
    def __init__(self, width, frames_dir):
        self.width = width
        self.height = 0
        self.frames_dir = frames_dir


    def set_width(self, frame):
        self.height = frame.shape[0] // self.width


    def render(self):
        for frame in self._convert_all_frames(self.frames_dir):
            self.set_width(frame)
            self._draw(frame)
            time.sleep(0.025)
        print(CLEAR_CODE)


    def _draw(self, arr):
        print(REFRESH_CODE)
        print('\n'.join(f''.join(self.set_ascii_color(arr[i]) 
                                 for i in range(self.width * x, self.width * (x + 1))) for x in range(self.height)), flush=True)


    def _convert_all_frames(self, dir):
        executor = ProcessPoolExecutor(max_workers=WORKERS) 
        sorted_files = sorted([os.path.join(dir, f) for f in os.listdir(dir)], key=lambda x: int(re.sub('[^0-9]', '', x)))
        self.num_frames = len(sorted_files)
        frames = []

        for f in tqdm(executor.map(self.set_frame_ascii, sorted_files, chunksize=CHUNK_SIZE), 
                      total=self.num_frames,
                      desc='Converting frames to ascii'):
            frames.append(f)
        
        print(RESET_CODE)
        return frames
    

    def set_frame_ascii(self, file):
        img = Image.open(file).convert('RGB')
        img_arr = np.asarray(img, dtype=np.uint8)
        return img_arr.reshape(-1, img_arr.shape[-1])


    def set_ascii_color(self, rgb):
        return f'{fg_code(rgb)}{TILE}{END_CODE}'
