import json
from sys import argv
from setup import read_env_file, setup_chrome_driver, setup_url_list

""" Setup everything needed for the program to run """
envVars = read_env_file()
urlList = setup_url_list(argv)
driver = setup_chrome_driver()

""" STUB: Perform your automated operations here... """
for url in urlList:
    driver.get(url)

# Write the performance log to disk as "performance_log.json"
perfLog = driver.get_log('performance')
perfLogFile = open('performance_log.json', 'w')
perfLogFile.write(json.dumps(perfLog))

driver.quit()
