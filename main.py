from argparse import ArgumentParser
from terminal import Renderer
from frames import FrameDownloader


FRAMES_DIR = './frames'
PIXEL_FRAMES_DIR = './pixel_frames'


if __name__ == '__main__':
    parser = ArgumentParser(description='Convert youtube videos into command line animations')
    parser.add_argument('-r', '--resolution', help='resolution of the display', required=True)
    parser.add_argument('-u', '--url', help='url of the youtube video',required=True)
    parser.add_argument('-f', '--fps', help='fps of the animation', default=30)

    args = vars(parser.parse_args())

    resolution = int(args['resolution'])
    url = args['url']
    fps = int(args['fps'])

    frame = FrameDownloader(resolution, FRAMES_DIR, PIXEL_FRAMES_DIR)
    term = Renderer(resolution, PIXEL_FRAMES_DIR, fps)

    frame.fetch_frames(url)
    term.render()
