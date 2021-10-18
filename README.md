# Auto Downloader Core
This is a starter project offers you the foundation for building a program that automates browser-based file downloading for you using [Python](https://python.org) and [Selenium](https://selenium.dev).

*Things to note...*
- *The following commands may differ depending on your Python version, operating system, and environment setup.*
- *This was only tested with Python 3.8.2 & 3.8.5, macOS Catalina & Big Sur, and ChromeDriver 94.0.4606.61.*

## Setup
1. Download and setup [ChromeDriver](https://chromedriver.chromium.org/downloads).
2. Setup your virtual environment and activate it. The command is probably along the lines of:  
`source .venv/bin/activate`
3. Install dependencies:  
`pip3 install -r requirements.txt`

## Running The Program
There are two ways to run the program:

You can pass in a simple series of command line arguments where each argument is a URL like so:
```
python3 main.py https://google.com https://stackoverflow.com https://youtube.com
```

Or you can pass in a text file for URLs you want to work with with the `-l` flag:
```
python3 main.py -l list.txt
```

Each line in the text file should only have one URL. For example, the contents of one could look like:
```
https://google.com
https://stackoverflow.com
https://youtube.com
```

### Using Environment Variables
You can pass in environment variables like so:
```
FOO=bar BAZ=qux python3 main.py https://reddit.com
```

Or you can define environment variables in a `.env` file at the root of the project. Each line in this file should represent an environment value like `{KEY}={VALUE}`.

To get the equivalent behavior from the previous example, the file should be written and formatted like so:
```
FOO=bar
BAZ=qux
```

Then all you would need to do is run the program without passing in the environment variables through the command line:
```
python3 main.py https://reddit.com
```

Note that the `.env` file will be ignored by Git, so if you want to commit it, you will need to remove it from `.gitignore`. Generally this file is intended to hold private information, so think twice before you commit it!

## Other Pre-Installed Dependencies
The following dependencies are available to you by default as they have a good chance of being useful:
- [Beautiful Soup](https://pypi.org/project/beautifulsoup4)
- [Requests](https://pypi.org/project/requests)

## Example
As a proof of concept, you can see this being used to build a Twitch VOD downloader on the [`twitch` branch](https://github.com/mattlean/auto-downloader-core/tree/twitch).