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
```
python main.py -r <resolution> -f <fps-optional> -u <youtube url>
```
Since the characters in the terminal are taller than they are wide, `<resolution>` only changes the width since the height is automatically calculated to maintain the original aspect ratio.

The fps of the animation is the same as the video, but you can optionally set your own. However, the actual fps depends on the resolution, the terminal, and your computer.

`-r 280` should maintain 30fps while `-r 360` should maintain 24fps but YMMV.

Depending on the resolution you may need to zoom out with `ctrl +-` or `ctrl scroll`. You may also need to mess around with your terminal fonts/colors to get it nice looking.

# Example

```
python main.py -r 240 -u https://www.youtube.com/watch?v=NWQKiefZ-XI
```

![race](./img/race.png)

# TODO

- Add different rendering options such as ascii, greyscale, etc
- Option to provide a video file instead of Youtube
- Catching signals to run cleanup
- Audio?
