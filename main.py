#!/usr/bin/env python3
import tkinter as tk
from videoprops import get_video_properties
import os, re
import subprocess

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

#Log item to .txt file
def log_output(thing, vStatus):
    with open("UltrawideBoss.txt", "a") as outF:
        outF.write(thing + '\n')
        outF.write(f'''Resolution: {vStatus['width']}x{vStatus['height']}''' + '\n')
        outF.write('\n')
        outF.close

#Log errors to .txt file
def log_error(thing):
    with open("UltrawideBoss.txt", "a") as outF:
        outF.write(thing + '\n')
        outF.write('This file is not a readable video format, skipping! \n')
        outF.write('Check FFmpeg documentation for valid file formats - https://ffmpeg.org/ffmpeg-formats.html \n')
        outF.write('\n')
        outF.close

#Scan for video files listed in directory_scan and list ones that are not ultra-wide format
def library_scan():
    for item in directory_scan():
        try:
            vProp = get_video_properties(item)
            if vProp['width'] / vProp['height'] < 2.37:
                print(item)
                print(f'''Resolution: {vProp['width']}x{vProp['height']}''')
                log_output(item, vProp)
            else:
                continue
        #Handling of unexpected character sets
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

#Call functions
library_scan()