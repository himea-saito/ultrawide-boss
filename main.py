#!/usr/bin/env python3
import tkinter as tk
import videodetection #queuehandling,  #transcoding

#GUI
#window = tk.Tk()
#title = tk.Label(text="Ultrawide Boss")
#title.pack()

#Indicate the directory path to scan
print('Please enter the full direct file path to the directory you want to scan.')
library_input = input("Directory to scan: ")

#Call functions
#auto_crop = input("Do you want to automatically crop detected videos? ")
#if auto_crop == 'Yes' or 'yes' or 'y':
    #library_scan_and_crop()
#if auto_crop == 'No' or 'no' or 'n':
    #library_scan()
#else:
    #print('Please answer yes or no')

crop = videodetection.media_detection(library_input).split('x')
##NOTE TO SELF: THIS IS OUTPUTTING A LIST OF STRINGS FOR SOME REASON##
print(crop)