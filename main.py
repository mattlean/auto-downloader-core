import json
from sys import argv
from setup import readEnvFile, setupChromeDriver, setupURLList

""" Setup everything needed for the program to run """
envVars = readEnvFile()
urlList = setupURLList(argv)
driver = setupChromeDriver()

""" STUB: Perform your automated operations here... """
for url in urlList:
    driver.get(url)

# Write the performance log to disk as "performance_log.json"
perfLog = driver.get_log('performance')
perfLogFile = open('performance_log.json', 'w')
perfLogFile.write(json.dumps(perfLog))

driver.quit()
