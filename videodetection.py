#!/usr/bin/env python3

from videoprops import get_video_properties
import os, re, subprocess, logging
from statistics import mode

#Return the most common value in a list
def most_common(item):
    return mode(item)

def resolution(item):
    vProp = get_video_properties(item)
    x = vProp['width']
    y = vProp['height']
    return x, y

#Scan for video files listed in directory_scan and list ones that are not ultra-wide format
def media_detection(item):
    try:
        res = [resolution(item)[0], resolution(item)[1]]
        if res[0] / res[1] < 2.37:
            crop_region = detectBars(item)
            cropx = crop_region[0]
            cropy = crop_region[1]
            res1 = res[0]
            res2 = res[1]
            crop_size = str(str(cropx) + 'x' + str(cropy))
            print(item)
            print('Resolution: ' + str(res))
            logging.log_output(item, res)
            if crop_region != 0:
                logging.log_crop(crop_size)
            return [cropx, cropy, res1, res2]
        else:
            print(item)
            print('Already ultrawide! Skipping.')
    #Handling of unexpected character sets
    ###NOTE TO SELF: ADD ERROR HANDLING IF FILE IS NOT WRITABLE###
    except UnicodeEncodeError:
        print('Unexpected character set in Unicode file format!!')
        print("This error was logged without a file name because I couldn't print it!")
        with open("UltrawideBoss.txt", "a") as outF:
            outF.write('Unexpected character set in Unicode file format!! \n')
            outF.write("This error was logged without a file name because I couldn't print it! \n")
            outF.close
    #Continue if the file is not a video format https://ffmpeg.org/ffmpeg-formats.html
    ##NOTE TO SELF: THIS EXCEPTION NEEDS TO NOT BE GLOBAL##
    #except:
        #print(item)
        #print('This file is not a readable video format, skipping!')
        #logging.log_error(item)

#Returns a value of x by y pixels in a video file, determined by scanning one out of every 3600 (2 minutes@30fps) frames for black area, up to 100 frames
def detectBars(item):
    result = subprocess.Popen(["./ffmpeg/bin/ffmpeg.exe", "-skip_frame", "nokey", "-ss", "2", "-y", "-hide_banner", 
        "-i", item, "-vf", "select='not(mod(n,3600))'", "cropdetect", "-frames", "100", "-an", "-f", "null", "-"], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')
    match = re.findall("crop=[0-9]+:[0-9]+:[0-9]+:[0-9]+", result.stderr.read())
###NOTE TO SELF: ADD ERROR HANDLING IF FILE IS NOT A VALID VIDEO FORMAT###
    readResults = []
    xExtract = []
    yExtract = []
    for item in match:
        readResults.append(item)
    for entry in readResults:
        extract = entry.split(':')
        xExtract.append(int(extract[2]))
        yExtract.append(int(extract[3]))
    x = most_common(xExtract)
    y = most_common(yExtract)
    if x == 0 and y == 0:
        print('No black pixels detected.')
        return(0)
    else:
        print('Detected black pixels: ' + str(x) + 'x' + str(y))
        return [x, y]