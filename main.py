#!/usr/bin/env python3
import tkinter as tk
import os, pathlib, shutil, sys, traceback, threading, time, videodetection, transcoding

#GUI
#window = tk.Tk()
#title = tk.Label(text="Ultrawide Boss")
#title.pack()

#Indicate the directory path to scan
print('Please enter the full direct file path to the directory you want to scan.')
library_input = input("Directory to scan: ")
transcode = input("Would you like to transcode the video(s) automatically?: ")

#Primary Functions
def main():
    for item in directory_scan(library_input):
        pulledvals = videodetection.media_detection(item)
        cropx = pulledvals[0]
        cropy = pulledvals[1]
        if transcode == 'Yes':
            #Folder for output transcoded video files
            #Creates a temporary directory for files being worked on
            cpfolder = input("Directory for transcoded videos: ")
            tempfolder = 'activecoding'
            activevideo = os.path.basename(item)
            path = os.path.join(cpfolder, tempfolder)
            fullpath = os.path.join(path, activevideo)
            if os.path.exists(fullpath): #Check if file exists before copying, error handling
                do = 'Nothing'
            else:
                print('Copying video file to transcoding folder.')
                os.mkdir(path) #Create temporary folder
                CPprogress(item, fullpath)
            ##ADDITIONAL FUNCTIONS FOR OTHER CONFIGS NOT USING NVIDIA WILL BE ADDED LATER##      
            if transcoding.cropNvidia(fullpath, cropx, cropy) == 0:
                try:
                    finished_video = str(fullpath) + "-RemuxUWB" + ".m4v"
                    shutil.move(finished_video, cpfolder) #Move transcoded file to directory when completed
                    os.remove(fullpath) #Remove copied video file
                    os.rmdir(path) #Remove temporary folder
                    print('Transcode completed and temporary files have been cleaned up.')
                except:
                    traceback.print_exc(limit=None, file=None, chain=True)
                    print('Transcode completed, but something went wrong with cleanup.')
            else:
                print('Process returned error code, transcode was not finished.')
        if transcode == 'No':
            print('Item was not transcoded.')
            continue

#Create a list of all files in the directory and subdirectories
def directory_scan(library_input):
    for root,dirs,files in os.walk(library_input):
        dirs.sort()
        files.sort()
        for file in files:
            yield(os.path.join(root, file))

#Progress bar for shutil copy
##Copied from https://stackoverflow.com/questions/274493/how-to-copy-a-file-in-python-with-a-progress-bar
############################
progressCOLOR = '\033[38;5;33;48;5;236m' 
finalCOLOR =  '\033[38;5;33;48;5;33m'
BOLD    = '\033[1m'
UNDERLINE = '\033[4m'
CEND    = '\033[0m'

def getPERCECENTprogress(source_path, destination_path):
    time.sleep(.24)
    if os.path.exists(destination_path):
        while os.path.getsize(source_path) != os.path.getsize(destination_path):
            sys.stdout.write('\r')
            percentagem = int((float(os.path.getsize(destination_path))/float(os.path.getsize(source_path))) * 100)
            steps = int(percentagem/5)
            copiado = int(os.path.getsize(destination_path)/1000000)# Should be 1024000 but this get's equal to Thunar file manager report (Linux - Xfce)
            sizzz = int(os.path.getsize(source_path)/1000000)
            sys.stdout.write(("         {:d} / {:d} Mb   ".format(copiado, sizzz)) +  (BOLD + progressCOLOR + "{:20s}".format('|'*steps) + CEND) + ("   {:d}% ".format(percentagem))) # BG progress
            #STYLE#sys.stdout.write(("         {:d} / {:d} Mb   ".format(copiado, sizzz)) +  (BOLD + BlueCOLOR + "▐" + "{:s}".format('█'*steps) + CEND) + ("{:s}".format(' '*(20-steps))+ BOLD + BlueCOLOR + endBLOCK+ CEND) +("   {:d}% ".format(percentagem))) #STYLE# # BG progress# closer to GUI but less compatible (no block bar with xterm) # requires utf8 coding header
            sys.stdout.flush()
            time.sleep(.01)

def CPprogress(SOURCE, DESTINATION):
    if os.path.isdir(DESTINATION):
        dst_file = os.path.join(DESTINATION, os.path.basename(SOURCE))
    else: dst_file = DESTINATION
    print (" ")
    print (BOLD + UNDERLINE + "FROM:" + CEND + "   " + str(SOURCE))
    print (BOLD + UNDERLINE + "TO:" + CEND + "     " + str(dst_file))
    print (" ")
    threading.Thread(name='progresso', target=getPERCECENTprogress, args=(SOURCE, dst_file)).start()
    shutil.copy2(SOURCE, DESTINATION)
    time.sleep(.02)
    sys.stdout.write('\r')
    sys.stdout.write(("         {:d} / {:d} Mb   ".format((int(os.path.getsize(dst_file)/1000000)), (int(os.path.getsize(SOURCE)/1000000)))) +  (BOLD + finalCOLOR + "{:20s}".format('|'*20) + CEND) + ("   {:d}% ".format(100))) # BG progress 100%
    #STYLE#sys.stdout.write(("         {:d} / {:d} Mb   ".format((int(os.path.getsize(dst_file)/1000000)), (int(os.path.getsize(SOURCE)/1000000)))) +  (BOLD + BlueCOLOR + "▐" + "{:s}{:s}".format(('█'*20), endBLOCK) + CEND) + ("   {:d}% ".format(100))) #STYLE# # BG progress 100%# closer to GUI but less compatible (no block bar with xterm) # requires utf8 coding header
    sys.stdout.flush()
    print (" ")
    print (" ")
#############################

###Initiate Script###
main()