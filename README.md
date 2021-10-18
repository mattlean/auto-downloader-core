# Twitch VOD Downloader
This is a proof of concept for [Auto Downloader Core](https://github.com/mattlean/auto-downloader-core) that automates the downloading of [Twitch](https://twitch.tv) VODs using [Python](https://python.org) and [Selenium](https://selenium.dev).

*Things to note...*
- *The following commands may differ depending on your Python version, operating system, and environment setup.*
- *This was only tested with Python 3.8.2 & 3.8.5, macOS Catalina & Big Sur, and ChromeDriver 94.0.4606.61.*

## How This Works
Twitch uses [HTTP Live Streaming](https://developer.apple.com/streaming) (also known as HLS) which is a very common way to deliver streaming video these days, so the video is sent to the browser as several fragments.

Before starting the video, Twitch will send down several `.m3u8` files that index all of the `.ts` fragments that compose the entire livestream VOD. Each `.m3u8` file corresponds to a particular video quality:

- chunked (highest quality possible that varies depending on the streamer's setup)
- 1080p60 (1080p 60fps)
- 900p60 (900p 60fps)
- 720p60 (720p 60fps)
- 720p30 (720p 30fps)
- 480p30 (480p 30fps)
- 360p30 (360p 30fps)
- 160p30 (160p 30fps)

This program will use Selenium to open a controlled [Google Chrome](https://google.com/chrome) process and scrape the network requests for the incoming `.m3u8` files. It will then figure which one corresponds to the highest quality, read it to figure out where all of the `.ts` fragments are, and then proceed to download all of them locally in a folder.

Once all of the `.ts` fragments are downloaded, this program will then stitch all of them together using `ffmpeg` which will then output the VOD as an `.mp4` file.

It will continue to repeat this process until all requested VOD URLs are processed.

*Note that there are much more optimal ways to download a Twitch VOD, but this project is just an experimental solution that strives to retrieve the `.m3u8` and `.ts` files in the most "human-like" way possible.*

## Setup
1. Download and setup [ChromeDriver](https://chromedriver.chromium.org/downloads).
2. Download and install [`ffmpeg`](https://ffmpeg.org).
2. Setup your virtual environment and activate it. The command is probably along the lines of:  
`source .venv/bin/activate`
3. Install dependencies:  
`pip3 install -r requirements.txt`

## Running The Program
There are two ways to run the program:

You can pass in a simple series of Twitch VOD links like so:
```
python3 tvd.py https://www.twitch.tv/videos/1175340925 https://www.twitch.tv/videos/1179438939
```

Or you can pass in a text file for Twitch VOD URLs you want to work with with the `-l` flag:
```
python3 tvd.py -l list.txt
```

Each line in the text file should only have one URL. For example, the contents of one could look like:
```
https://www.twitch.tv/videos/1175340925
https://www.twitch.tv/videos/1179438939
https://www.twitch.tv/videos/1178943795
```

The video that will generate will be `{VOD_ID}.mp4`. So for example, if the input URL was `https://www.twitch.tv/videos/1175340925`, its corresponding video will be named `1175340925.mp4`.
