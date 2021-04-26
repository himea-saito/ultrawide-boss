#!/usr/bin/env python3
import tkinter as tk
from videoprops import get_video_properties
from statistics import mode
import os, re, subprocess

#GUI
#window = tk.Tk()
#title = tk.Label(text="Ultrawide Boss")
#title.pack()

#Indicate the directory path to scan
print('Please enter the full direct file path to the directory you want to scan.')
library_input = input("Directory to scan: ")

#Create a list of all files in the directory and subdirectories
def directory_scan():
    for root,dirs,files in os.walk(library_input):
        dirs.sort()
        files.sort()
        for file in files:
            yield(os.path.join(root, file))

#Log resolution to .txt file
def log_output(item, vStatus):
    with open("UltrawideBoss.txt", "a") as outF:
        outF.write(item + '\n')
        outF.write(f'''Resolution: {vStatus['width']}x{vStatus['height']}''' + '\n')
        outF.write('\n')
        outF.close

#Log non-video file to .txt file
def log_error(item):
    with open("UltrawideBoss.txt", "a") as outF:
        outF.write(item + '\n')
        outF.write('This file is not a readable video format, skipping! \n')
        outF.write('Check FFmpeg documentation for valid file formats - https://ffmpeg.org/ffmpeg-formats.html \n')
        outF.write('\n')
        outF.close

#Log region to be cropped to .txt file
def log_crop(item):
    with open("UltrawideBoss.txt", "a") as outF:
        outF.write("Black pixel region detected : " + str(item[0]) + "x" + str(item[1]) + '\n')
        outF.write('\n')
        outF.write('\n')
        outF.close

#Return the most common value in a list
def most_common(list):
    return(mode(list))

#Returns a value of x by y pixels in a video file and scan 60 (~2.5 seconds) frames for consistent black color value
def detectBars(item):
    result = subprocess.Popen(["./ffmpeg/bin/ffmpeg.exe", "-skip_frame", "nokey", "-ss", "2", "-y", "-hide_banner", 
        "-i", item, "-vf", "cropdetect", "-frames", "60", "-an", "-f", "null", "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')
    match = re.findall("crop=[0-9]+:[0-9]+:[0-9]+:[0-9]+", result.stderr.read())
###NOTE TO SELF: ADD ERROR HANDLING IF FILE DOES NOT YIELD PIXEL RESULTS FOR WHATEVER REASON###
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
        return(list([x, y]))

#Scan for video files listed in directory_scan and list ones that are not ultra-wide format
def library_scan():
    for item in directory_scan():
        try:
            vProp = get_video_properties(item)
            if vProp['width'] / vProp['height'] < 2.37:
                print(item)
                print(f'''Resolution: {vProp['width']}x{vProp['height']}''')
                crop_region = detectBars(item)
                log_output(item, vProp)
                if crop_region != 0:
                    log_crop(crop_region)
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
        except:
            print(item)
            print('This file is not a readable video format, skipping!')
            log_error(item)

#Do the same as library_scan but also automatically crop detected black pixel regions
def library_scan_and_crop():
    print("Sorry, this feature isn't implemented yet!")

#Call functions
#auto_crop = input("Do you want to automatically crop detected videos? ")
#if auto_crop == 'Yes' or 'yes' or 'y':
    #library_scan_and_crop()
#if auto_crop == 'No' or 'no' or 'n':
    #library_scan()
#else:
    #print('Please answer yes or no')

library_scan()