# Setup
Since this project uses 24-bit true color, visit this [gist](https://gist.github.com/kurahaupo/6ce0eaefe5e730841f03cb82b061daa2) to see if your terminal supports it. Most modern terminals should, but maybe you like your retro stuff.


To install the Python packages run
```
pip install -r requirements.txt
```

This project also uses FFmpeg which handles the frame extraction from the videos.

To check if you have it installed already, run
```
ffmpeg -version
```

If you don't have it installed, follow the links below.

- [Windows](https://phoenixnap.com/kb/ffmpeg-windows)
- [Linux](https://phoenixnap.com/kb/install-ffmpeg-ubuntu)
- [MacOS](https://phoenixnap.phoenixnap/kb/ffmpeg-windows)

# Usage
> **_Warning_**: Do not decrease the terminal size while a video is playing!
```
python main.py -[flags] -u <youtube url>
```

## Flags

> `-r <resolution: int> [optional]`

The pixel width of the display. If this flag is not set, then it will default to the current width of your terminal.

> `-f <fps: int> [optional]`

The fps at which to split the video and replay in the terminal. Since videos download at <= 30fps, setting it too high will result in a lot of duplicate frames.

> `-p <performance test <: toggle> `

Switch to a different rendering algorithm. Performs worse than the default algorithm in most cases :(

> `-s <stats: toggle> `

Add the flag to display a duration bar, fps, and elapsed time at the bottom of the video. Can be a little buggy with when enabled with the `-p` flag.

> `-u <youtube url: str> [required]`

URL to a video. Some videos may fail to download due to restrictions set by Youtube.


## Performance
The framerate will depend on your computer, the terminal you are using, and resolution. A GPU accelerated terminal like [WezTerm](https://wezfurlong.org/wezterm/index.html) or [Windows Terminal](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701) performs the best here.

# Example

```
python main.py -p -s -u https://www.youtube.com/watch?v=uMeR2W19wT0
```

![example](./img/example.png)

# TLDR
python is slow, using c++ next time
