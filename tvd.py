import json
import os
import re
import requests
import subprocess
from enum import Enum
from sys import argv
from setup import read_env_file, setup_chrome_driver, setup_url_list
from util import prefixPrintMsg, suffixException

""" Setup everything needed for the program to run """
envVars = read_env_file()
urlList = setup_url_list(argv)

""" Perform your automated operations here... """
for url in urlList:
    vodID = url.split('/')[-1]

    print(prefixPrintMsg(f'Processing for {vodID or url} will now start!'))
    print(prefixPrintMsg('Please allow ChromeDriver to scrape for a moment...'))

    # Run ChromeDriver & read network requests
    driver = setup_chrome_driver(True, {'traceCategories': 'devtools.timeline', 'enableNetwork': True})
    driver.get(url)
    perfLog = driver.get_log('performance')
    driver.quit()

    # Find .m3u8 file that corresponds to best quality
    m3u8 = None
    clintStevens = ''

    qualityPriorityMap = {
        'chunked': 8,
        '1080p60': 7,
        '900p60': 6,
        '720p60': 5,
        '720p30': 4,
        '480p30': 3,
        '360p30': 2,
        '160p30': 1,
    }
    qualities = qualityPriorityMap.keys()

    for item in perfLog:
        potentialM3u8 = json.loads(item.get('message', {})).get('message', {}).get('params', {}).get('args', {}).get('data', {}).get('url', '')
        if potentialM3u8.endswith('.m3u8'):
            potentialM3u8Split = potentialM3u8.split('/')
            currQuality = potentialM3u8Split[-2]

            if currQuality in qualities:
                if qualityPriorityMap.get(currQuality, 0) > qualityPriorityMap.get(clintStevens, 0):
                    clintStevens = currQuality
                    m3u8 = potentialM3u8

    filePrefix = ''

    if not m3u8:
        raise Exception(suffixException('Could not find a .m3u8 file.'))
    else:
        filePrefixSplit = m3u8.split('/')[:-1]
        filePrefix = '/'.join(filePrefixSplit) + '/'

    # Download .m3u8 file
    res = requests.get(m3u8)
    res.raise_for_status()

    if len(res.text) < 1:
        raise Exception(suffixException('.m3u8 file was empty.'))

    # Find .ts files
    tsFileRegex = re.compile(r'\d*.ts')
    tsFiles = tsFileRegex.findall(res.text)

    tsFilesLen = len(tsFiles)
    if tsFilesLen < 1:
        raise Exception(suffixException('.ts files were not found in .m3u8 file.'))

    print(prefixPrintMsg('Scraping was successful!'))
    print(prefixPrintMsg('Download for VOD fragments will now commence...'))

    # Create folder for downloaded .ts files
    tsDlFolder = f'ts_{clintStevens}_{vodID or url}'
    if not os.path.exists(tsDlFolder):
        os.makedirs(tsDlFolder)

    # Generate meta file
    metaFile = open(f'{tsDlFolder}/meta.json', 'w')
    metaFile.write(json.dumps({
        'id': vodID,
        'url': url,
        'quality': clintStevens,
        'filePrefix': filePrefix,
        'm3u8': m3u8,
    }))

    # Download .ts files
    for i, tsFile in enumerate(tsFiles):
        print(prefixPrintMsg(f'Downloading {vodID or url}... ({i + 1}/{tsFilesLen})'))
        res = requests.get(f'{filePrefix}{tsFile}')
        res.raise_for_status()
        localTsFile = open(f'{tsDlFolder}/{tsFile}', 'wb')
        for chunk in res.iter_content(100000):
            localTsFile.write(chunk)

    print(prefixPrintMsg(f'{vodID or url} fragments were successfully downloaded!'))
    print(prefixPrintMsg('Stitching VOD fragments will now commence...'))

    # Generate the input list file needed for stitching
    inputListLoc = f'{tsDlFolder}/ffmpeg_input_list.txt'
    for i, tsFile in enumerate(tsFiles):
        if i == 0:
            inputListFile = open(inputListLoc, 'w')
            inputListFile.write(f"file '{tsFile}'")
        else:
            inputListFile = open(inputListLoc, 'a')
            inputListFile.write(f"\nfile '{tsFile}'")

    # Stitch the .ts files into an .mp4
    returnCode = -1
    try:
        returnCode = subprocess.call(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', inputListLoc, '-c', 'copy', f'{vodID or url}.mp4'])
    except:
        raise Exception(suffixException('Something went wrong with ffmpeg.'))

    if returnCode != 0:
        raise Exception(suffixException(f'Something went wrong with ffmpeg. (Return Code {returnCode})'))

    print(prefixPrintMsg(f'Stitching {vodID or url} was successful!'))
    print(prefixPrintMsg(f'{vodID or url}.mp4 was generated! POGGERS'))

print(prefixPrintMsg('Job\'s done!!! EZ'))
