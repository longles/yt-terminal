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

**Disclaimer**: This program can create GB sized folders of images

```
python main.py -r <resolution> -u <youtube url>
```
Depending on the resolution you may need to zoom out with `ctrl +-` or `ctrl scroll`. You may also need to mess around with your terminal fonts/colors to get it nice looking. 

For reference, the image below is in the Courier New font using
```
python main.py -r 100 -u https://www.youtube.com/watch?v=QH2-TGUlwu4
```



![meow](./img/nyan_cat.png)