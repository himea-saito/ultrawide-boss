#!/usr/bin/env python3

##This file creates a faux Handbrake CLI queue because it doesn't natively support it##

##THIS MODULE IS UNFINISHED DO NOT LOAD##

def list_add(item):
    print("Video transcode completed, adding to completed list...")
    with open ("UltrawideBossTranscodeFinished.log", "a") as outF:
        outF.write(str(item))

def list_detect(item):
    with open ("UltrawideBossTranscodeFinished.log," "a") as inF:
        for line in inF:
            if line == item:
                line.next()
                continue
            else:
                ##NOTE TO SELF: ADD HANDBRAKE TRANSCODE FUNCTION HERE##