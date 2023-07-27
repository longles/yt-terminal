from PIL import Image
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

import numpy as np
import time
import os
import re


# ANSI codes
END_CODE = '\033[0;0m'
REFRESH_CODE = '\033[H'
RESET_CODE = '\033c'

TILE = ' '
PROJECT_NAME = 'yt-terminal'


"""
ANSI sequence to set the character color
"""
def fg_code(rgb: tuple[np.uint8, np.uint8, np.uint8]) -> str:
    return f'\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m'


"""
ANSI sequence to set the background color
"""
def bg_code(rgb: tuple[np.uint8, np.uint8, np.uint8]) -> str:
    return f'\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m'


"""
Turns text rainbow colored
"""
def rainbow(text: str) -> str:
    output = ''
    rainbow = [
        (148, 0, 211), (75, 0, 130), (0, 0, 255),
        (0, 255, 0), (255, 255, 0), (255, 127, 0),
        (255, 0 , 0)
    ]

    for i in range(len(text)):
        output += f'{fg_code(rainbow[i % len(rainbow)])}{text[i]}{END_CODE}'

    return output


"""
Handles converting frames into ascii characters and rendering onto a terminal interface
"""
class Renderer:
    def __init__(self, width: int, frames_dir: str, fps: int, workers: int, chunk_size: int) -> None:
        self.width = width
        self.height = 0
        self.frames_dir = frames_dir
        self.fps = fps
        self.workers = workers
        self.chunk_size = chunk_size


    """
    Sets the height using a 2D numpy array generated from image frames
    """
    def set_height(self, frame: np.ndarray) -> None:
        self.height = frame.shape[0] // self.width


    """
    Rendering loop that prints the ascii characters to the terminal and maintains a consistent FPS limit.
    """
    def render(self) -> None:
        setup = True
        frames = self._convert_all_frames(self.frames_dir)

        for frame in tqdm(frames, total=self.num_frames, desc=rainbow(PROJECT_NAME),
                          unit=' frames', ncols=self.width, colour='WHITE'):
            curr_time = time.perf_counter()
            if setup:
                setup = False
                self.set_height(frame)
                print(RESET_CODE)

            self._draw(frame)
            while time.perf_counter() < (curr_time + 1 / self.fps):  # more accurate than time.sleep()
                pass


    """
    Printing the ascii characters using a generator expression
    """
    def _draw(self, arr: np.ndarray) -> None:
        print(REFRESH_CODE)
        print('\n'.join(f''.join(
            self._set_ascii_color(arr[i])
            for i in range(self.width * x, self.width * (x + 1)))
            for x in range(self.height)), flush=True)


    """
    Spawns several processes (cuz multithreading in Python is a doozy) to each convert frame into ascii characters
    """
    def _convert_all_frames(self, dir: str) -> list:
        executor = ProcessPoolExecutor(max_workers=self.workers)
        files = [os.path.join(dir, f) for f in os.listdir(dir)]
        sorted_files = sorted(files, key=lambda x: int(re.sub('[^0-9]', '', x)))
        self.num_frames = len(sorted_files)
        frames = []

        for f in tqdm(executor.map(self._set_frame_ascii, sorted_files, chunksize=self.chunk_size),
                      total=self.num_frames, desc='Converting frames to ascii', colour='WHITE', unit=' frames'):
            frames.append(f)

        print(RESET_CODE)
        return frames


    """
    Reading RGB pixel data from the video frames into a 2D numpy array [width x height [r, g, b]]
    """
    def _set_frame_ascii(self, file: str) -> np.ndarray:
        img = Image.open(file).convert('RGB')
        img_arr = np.asarray(img, dtype=np.uint8)
        return img_arr.reshape(-1, img_arr.shape[-1])


    """
    Sets the color of the tile
    """
    def _set_ascii_color(self, rgb: tuple[np.uint8, np.uint8, np.uint8]) -> str:
        return f'{bg_code(rgb)}{TILE}{END_CODE}'
