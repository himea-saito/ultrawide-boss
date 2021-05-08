#!/usr/bin/env python3

#Crop video with detected black pixel area from detectBars function
###THIS IS NOT FINISHED###
def crop1080Nvidia(item, crop_area):
    widthCrop = crop_area[0]
    heightCrop = crop_area[1]
    crop = subprocess.Popen(["./ffmpeg/handbrake/HandBrakeCLI.exe", "-i", str(item), "--preset-import-file", "./presets/himea1080poptimizednvidia.json", 
        "--crop", str(widthCrop) + ':' + 'ih-' + str(heightCrop) + '"', str(item) + "-RemuxUWBoss-" + ".m4v"])