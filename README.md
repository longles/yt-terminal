# Setup

To install the Python packages run
```
pip install -r requirements.txt
```

This project also uses FFmpeg which handles the frame extraction from the videos

To check if you have it installed already, run
```
ffmpeg -version
```

If you don't have it installed, follow the links below
### Windows
https://phoenixnap.com/kb/ffmpeg-windows

### Linux
https://itsfoss.com/ffmpeg/

# Usage

**Disclaimer**: The RAM and disk usage of this program can grow quite fast

```
python main.py -r <resolution> -f <fps> -u <youtube url>
```
Depending on the resolution you may need to zoom out with `ctrl +-` or `ctrl scroll`. You may also need to mess around with your terminal fonts/colors to get it nice looking. 

The default fps cap is 30, but you may to change it depending on the resolution. High resolutions is more expensive to draw, and thus may need a higher fps cap to stay smooth.

For reference, the image below is in the Courier New font using
```
python main.py -r 200 -u https://www.youtube.com/watch?v=QH2-TGUlwu4
```

![meow](./img/nyan_cat.png)
