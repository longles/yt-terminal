from argparse import ArgumentParser

import terminal
import frames


FRAMES_DIR = './frames'
PIXEL_FRAMES_DIR = './pixel_frames'


# TODO: Add progress bars for pixelation
if __name__ == '__main__':
    parser = ArgumentParser(description='Convert youtube videos into command line animations')
    parser.add_argument('-w', '--width', help='set the width of the display')
    parser.add_argument('-l', '--height', help='set the height of the display')
    parser.add_argument('-u', '--url', help='url of the youtube video')

    args = vars(parser.parse_args())

    width = int(args['width'])
    height = int(args['height'])
    url = args['url']

    terminal = terminal.Renderer(width, height, PIXEL_FRAMES_DIR)
    frames = frames.FrameDownloader(width, height, FRAMES_DIR, PIXEL_FRAMES_DIR)

    frames.fetch_frames(url)
    terminal.render()
