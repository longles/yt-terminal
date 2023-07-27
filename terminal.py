from PIL import Image
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

import numpy as np
import time
import re

from utils.ansi import *
from utils.files import *
from utils.other import *


PROJECT_NAME = 'yt-terminal'

TILE = ' '


"""
Handles converting frames into ascii and rendering onto the terminal.
"""
class Renderer:
    def __init__(self, frames_dir: str, fps: int, workers: int, chunk_size: int, perf: bool, stats: bool) -> None:
        f = get_files(frames_dir)
        img = Image.open(f[0])

        self.frames = f
        self.width = img.width
        self.height = img.height
        self.fps = fps
        self.workers = workers
        self.chunk_size = chunk_size
        self.perf = perf
        self.stats = stats
        self.num_frames = len(f)


    """
    Runs the renderer.
    """
    def run(self):
        if self.perf:
            self.fast_render()
        else:
            self.render()


    """
    Rendering loop that prints the ascii characters to the terminal and maintains a consistent FPS limit. Progress bar is used
    to visualize current status. Uses _fast_render() to improve overall performance.
    """
    def fast_render(self) -> None:
        frames = self._convert_all_frames()
        prev_frame = np.full((self.width * self.height, 3), -1)
        t_height = get_terminal_dimensions()[1]

        self._fast_draw(frames[0], prev_frame)
        prev_frame = frames[0]

        for curr_frame in tqdm(frames[1:], total=self.num_frames, desc=rainbow(PROJECT_NAME),
                               unit=' frames', ncols=self.width - 1, colour='WHITE', disable=self.stats,
                               bar_format='%s{l_bar}{bar}{r_bar}%s%s' % (move_cursor(t_height - 1, 0), REFRESH_CODE, END_CODE)):

            curr_time = time.perf_counter()

            self._fast_draw(curr_frame, prev_frame)
            prev_frame = curr_frame

            while time.perf_counter() < (curr_time + 1 / self.fps):  # more accurate than time.sleep()
                pass


    """
    Rendering loop that prints the ascii characters to the terminal and maintains a consistent FPS limit. Progress bar is used
    to visualize current status.
    """
    def render(self) -> None:
        setup = True
        frames = self._convert_all_frames()

        for frame in tqdm(frames, total=self.num_frames, desc=rainbow(PROJECT_NAME),
                          unit=' frames', ncols=self.width, colour='WHITE', disable=self.stats):

            curr_time = time.perf_counter()

            if setup:
                setup = False
                print(REFRESH_CODE)

            self._draw(frame)

            while time.perf_counter() < (curr_time + 1 / self.fps):
                pass


    """
    Prints only characters that have changed since the last frame. Saves on the number of writes and takes advantage
    of vectorized numpy operations.
    """
    def _fast_draw(self, curr_frame: np.ndarray, prev_frame: np.ndarray) -> None:
        def idx_coords(i):
            return ceil_div(i, self.width), int(i % self.width)

        idx = np.nonzero(np.not_equal(curr_frame, prev_frame).any(axis=1))[0]
        print(''.join(self._set_coord_color(curr_frame[i], *idx_coords(i)) for i in idx), flush=True)


    """
    Prints the ascii characters using a generator expression.
    """
    def _draw(self, arr: np.ndarray) -> None:
        print(REFRESH_CODE)
        print('\n'.join(f''.join(
            self._set_ascii_color(arr[i])
            for i in range(self.width * x, self.width * (x + 1)))
            for x in range(self.height)), flush=True)


    """
    Spawns several processes (cuz multithreading in Python is a doozy) to each convert frame into ascii. Progress bar is used
    to visualize current status.
    """
    def _convert_all_frames(self) -> list:
        executor = ProcessPoolExecutor(max_workers=self.workers)
        sorted_frames = sorted(self.frames, key=lambda x: int(re.sub('[^0-9]', '', x)))
        frames = []

        for f in tqdm(executor.map(self._set_frame_ascii, sorted_frames, chunksize=self.chunk_size),
                      total=self.num_frames, desc='Converting frames to ascii', colour='WHITE', unit=' frames'):
            frames.append(f)

        print(RESET_CODE)
        return frames


    """
    Reads RGB pixel data from video frames into a 2D numpy array [width x height [r, g, b]].
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


    """
    Sets the color of the tile
    """
    def _set_coord_color(self, rgb: tuple[np.uint8, np.uint8, np.uint8], x: int, y: int) -> str:
        return f'{move_cursor(x, y)}{bg_code(rgb)}{TILE}{END_CODE}'
