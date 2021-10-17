import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def readEnvFile(envFileName = '.env'):
    """Attempt to read the .env file."""
    try:
        envFile = open(envFileName)
    except:
        # .env file was not found
        return None

    envVarList = envFile.read().splitlines()
    for envVar in envVarList:
        envVarKeyVal = envVar.split('=')

        if len(envVarKeyVal) == 2:
            os.environ[envVarKeyVal[0]] = envVarKeyVal[1]
    
    return os.environ

def setupChromeDriver():
    """Setup undetected ChromeDriver with performance log enabled."""
    # Make ChromeDriver undetected
    # Also some things you might want to consider...
    # https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver/41220267
    # https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')

    # Enable performance log
    # https://chromedriver.chromium.org/logging/performance-log
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    driver = webdriver.Chrome(desired_capabilities=caps, options=options)

    return driver

def setupURLList(argv):
    """Setup the URL list."""
    urlList = None
    mode = 'default'

    if len(argv) > 2:
        if argv[1] == '-l':
            # Populate url list from text file
            listFile = open(argv[2])
            urlList = listFile.read().splitlines()
            mode = 'file'

    if mode != 'file':
        # Populate url list from CLI args
        urlList = argv[1:]
    
    return urlList
