# Setup

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

**Disclaimer**: The RAM and disk usage of this program can grow quite fast.

```
python main.py -r <resolution> -f <fps-optional> -u <youtube url>
```
Depending on the resolution you may need to zoom out with `ctrl +-` or `ctrl scroll`. You may also need to mess around with your terminal fonts/colors to get it nice looking. 

The default fps is 30 since that is the typical framerate of Youtube videos.

For reference, the image below is captured from

```
python main.py -r 240 -u https://www.youtube.com/watch?v=NWQKiefZ-XI
```

![race](./img/race.png)
