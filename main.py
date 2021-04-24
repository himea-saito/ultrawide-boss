#!/usr/bin/env python3
import tkinter as tk
from videoprops import get_video_properties
import os, re

#GUI
#window = tk.Tk()
#title = tk.Label(text="Ultrawide Boss")
#title.pack()

#Indicate the directory path to scan
print('Please enter the full direct file path to the directory you want to scan.')
library_input = input("Directory to scan: ")

#Create a list of all files in the directory
def directory_scan():
    with os.scandir(library_input) as filename:
        for entry in filename:
            if entry.is_file():
                print(entry.name)
                yield os.path.join(library_input, entry.name)
            elif entry.is_dir():
                directory_scan()
            else:
                print("Unexpected object type in directory.")

#Scan for video files listed in directory_scan and list ones that are not ultra-wide format
def library_scan():
    for item in directory_scan():
        vProp = get_video_properties(item)
        if vProp['width'] / vProp['height'] < 2.37:
            print(f'''Resolution: {vProp['width']}x{vProp['height']}''')
            print('This video file is not ultra-wide!')

#Call functions
library_scan()