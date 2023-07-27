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

### Windows
https://phoenixnap.com/kb/ffmpeg-windows

### Linux
https://itsfoss.com/ffmpeg/


# Usage
> **_Warning_**: Do not change the terminal size while video is running!
```
python main.py -r <resolution [optional]> -f <fps [optional]> -u <youtube url>
```
If `resolution` is not provided, then the video is automatically adjusted to fit the terminal.

If `fps` is not provided, then the video runs at the frame rate of the youtube video.

# Example

```
python main.py -u https://www.youtube.com/watch?v=SjBOC94WHBQ
```

![example](./img/example.png)

# TODO

- Add different rendering options such as ascii lumosity, greyscale, etc
- Option to provide a video file instead of Youtube
- Catching signals to run cleanup
- Synced audio
- FFmpeg use GPU?
