#!/usr/bin/env python3
import tkinter as tk
from videoprops import get_video_properties
import os, re

#GUI
window = tk.Tk()
title = tk.Label(text="Ultrawide Boss")
title.pack()

#Library scan
library_input = input("Enter directory to scan: ")
libraryDir = library_input

def directory_scan():
    contents = os.listdir(libraryDir)
    for item in contents:
        if os.path.isdir(item):
            directory_scan()
        else:
            print(item)

def library_scan():
    videoRead = get_video_properties.read()
    videoSplit = videoRead.split()
    with os.scandir(directory_scan()) as listOfEntries:
        videoSplit for item in listOfEntries:
            if re.search("Resolution: /[0-9]{3,}×[0-9]{3,}/gm") for videoSplit == True:
                print(item)
