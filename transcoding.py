#!/usr/bin/env python3

import subprocess, traceback

#Crop video with detected black pixel area from detectBars function
#Help links https://stackoverflow.com/questions/37925840/python-monitoring-progress-of-handbrake
###THIS IS NOT FINISHED###
def cropNvidia(file, x, y):
    try:
        cmd = ["./handbrake/HandBrakeCLI.exe", "-i", str(file), 
            '-q', '18.0', '-r', 'auto', '-all-audio', '-all-subtitles',
            '--audio-copy-mask', 'aac,ac3,dtshd,dts,mp3',
            '--audio-fallback', 'ffac3', '-f', 'mp4', '--loose-anamorphic', '--modulus', '2',
            '-m', "--crop", str(y) + ':' + str(y) + ':' + str(x) + ':' + str(x),
            '-e', 'nvenc_h265', '--optimize', '-o', str(file) + "-RemuxUWB" + ".m4v"]
        for path in execute(cmd):
            print(path, end='')
        return 0
    except:
        traceback.print_exc(limit=None, file=None, chain=True)
        return 1

#This prints the STDOUT in real time
def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)