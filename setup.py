import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def read_env_file(envFileName = '.env'):
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

def setup_chrome_driver(enablePerfLogging = False, perfLogPrefs = None):
    """Setup undetected ChromeDriver."""
    # Make ChromeDriver undetected
    # Also some things you might want to consider...
    # https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver/41220267
    # https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')

    if (enablePerfLogging):
        # Enable performance log
        # https://chromedriver.chromium.org/logging/performance-log
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}

        if perfLogPrefs:
            options.add_experimental_option('perfLoggingPrefs', perfLogPrefs)

        return webdriver.Chrome(desired_capabilities=caps, options=options)
    else:
        return webdriver.Chrome(options=options)

def setup_url_list(argv):
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
