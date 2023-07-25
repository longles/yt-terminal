from argparse import ArgumentParser

import terminal
import frames


FRAMES_DIR = './frames'
PIXEL_FRAMES_DIR = './pixel_frames'


# TODO: Add progress bars for pixelation
if __name__ == '__main__':
    parser = ArgumentParser(description='Convert youtube videos into command line animations')
    parser.add_argument('-r', '--resolution', help='set the resolution of the display')
    parser.add_argument('-u', '--url', help='url of the youtube video')

    args = vars(parser.parse_args())

    resolution = int(args['resolution'])
    url = args['url']

    terminal = terminal.Renderer(resolution, resolution, PIXEL_FRAMES_DIR)
    frames = frames.FrameDownloader(resolution, resolution, FRAMES_DIR, PIXEL_FRAMES_DIR)

    frames.fetch_frames(url)
    terminal.render()
