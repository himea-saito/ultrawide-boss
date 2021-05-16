#!/usr/bin/env python3

import subprocess

#Crop video with detected black pixel area from detectBars function
#Help links https://stackoverflow.com/questions/37925840/python-monitoring-progress-of-handbrake
###THIS IS NOT FINISHED###
def crop1080Nvidia(file):
    cmd = ["./handbrake/HandBrakeCLI.exe", "-i", str(file), "--preset-import-file", 
        "./presets/himea1080poptimizednvidia.json", "--crop", 'default', '-e', 'nvenc_h265', '--optimze',
        '-o', str(file) + "-RemuxUWB" + ".m4v"]
    for path in execute([cmd, 'a']):
        print(path, end='')

def crop4kNvidia(file):
    cmd = ["./handbrake/HandBrakeCLI.exe", "-i", str(file), "--preset-import-file", 
        "./presets/himea4koptimizednvidia.json", "--crop", 'default', '-e', 'nvenc_h265', '--optimze',
        '-o', str(file) + "-RemuxUWB" + ".m4v"]
    for path in execute([cmd, 'a']):
        print(path, end='')

def Transcode_Auto_Size(height, file):
    if 900 <= height <= 1100:
        print('FHD resolution detected, transcoding in 1080p')
        if crop1080Nvidia(file) == 1:
            return 1
        else:
            return 0
    elif 2000 <= height <= 2400:
        print('4k resolution detected, transcoding in 2160p')
        if crop4kNvidia(file) == 1:
            return 1
        else:
            return 0
    else:
        print('No valid resolution detected for transcoding. Something unexpected happened.')

#This prints the STDOUT in real time
def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)