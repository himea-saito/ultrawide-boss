#!/usr/bin/env python3

from videoprops import get_video_properties
import os, re, subprocess, logging
from statistics import mode

#Create a list of all files in the directory and subdirectories
def directory_scan(library_input):
    for root,dirs,files in os.walk(library_input):
        dirs.sort()
        files.sort()
        for file in files:
            yield(os.path.join(root, file))

#Return the most common value in a list
def most_common(item):
    print('Test! ' + str(mode(item)))
    return mode(item)

#Scan for video files listed in directory_scan and list ones that are not ultra-wide format
def media_detection(library_input):
    for item in directory_scan(library_input):
        try:
            vProp = get_video_properties(item)
            resolution = str(str(vProp['width']) + 'x' + str(vProp['height']))
            if vProp['width'] / vProp['height'] < 2.37:
                crop_region = []
                crop_region.append(detectBars(item))
                cropx = [i[0] for i in crop_region]
                cropy = [i[1] for i in crop_region]
                crop_size = str(str(cropx) + 'x' + str(cropy))
                print(item)
                print('Resolution: ' + str(resolution))
                logging.log_output(item, resolution)
                if crop_region != 0:
                    logging.log_crop(crop_size)
                return crop_size
            else:
                continue
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

#Returns a value of x by y pixels in a video file and scan 60 (~2.5 seconds) frames for consistent black color value
def detectBars(item):
    result = subprocess.Popen(["./ffmpeg/bin/ffmpeg.exe", "-skip_frame", "nokey", "-ss", "2", "-y", "-hide_banner", 
        "-i", item, "-vf", "cropdetect", "-frames", "60", "-an", "-f", "null", "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')
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
        xstring = str(x)
        ystring = str(y)
        print('Detected black pixels: ' + xstring + 'x' + ystring)
        return [x, y]