#!/usr/bin/env python3

#Log resolution to .txt file
def log_output(item, resolution):
    with open("UltrawideBoss.log", "a") as outF:
        outF.write(item + '\n')
        outF.write('Resolution: ' + str(resolution) + '\n')
        outF.write('\n')
        outF.close

#Log non-video file to .txt file
def log_error(item):
    with open("UltrawideBoss.log", "a") as outF:
        outF.write(item + '\n')
        outF.write('This file is not a readable video format, skipping! \n')
        outF.write('Check FFmpeg documentation for valid file formats - https://ffmpeg.org/ffmpeg-formats.html \n')
        outF.write('\n')
        outF.close

#Log region to be cropped to .txt file
def log_crop(crop_size):
    with open("UltrawideBoss.log", "a") as outF:
        outF.write("Black pixel region detected : " + str(crop_size) + '\n')
        outF.write('\n')
        outF.write('\n')
        outF.close