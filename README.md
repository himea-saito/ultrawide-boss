# ultrawide-boss
Scans video librarires for files with hard-coded black bars for cinema to home formatting.


This is still a work in progress, however it is usable.


Beware that the auto-transcode function is extremely verbose right now and will only work with an Nvidia card installed.


How to use:

This will be an executable package later, but right now you will need to install the following separately:

-Python 3.7 or later

-VideoProps Python Module (https://pypi.org/project/get-video-properties/)

    --pip install -U get-video-properties (You can do this if you've installed Python scripts in path)

-Download these scripts as a zip and extract them to a custom directory of your choice.

Run main.py in python

-Enter the top level directory that you want the script to scan through for video files

    --e.g. C:\Users\Me\Videos\
    
-Choose if you want the script to automatically transcode video files for you (Yes/No)

    --If yes, choose where you want transcoded video files to be stored
    
        ---e.g. C:\Users\Me\Videos\Transcoded\
        
-Wait!

    --UWB will create a list of video files detected in the script root directory and what it did with them.
    
        ---UltrawideBoss.log
        
    --UWB detects black bars to crop by polling every 3600 video frames, up to 100.
    
    --If automatic transcode is selected, it wil copy the video file and then transcode it without the bars.
    
    --Beware that it may take several hours to transcode each video
    
    --Also beware that some movies and shows change their aspect ratio, which might create a false positive.
    
    --Make sure to check each transcoded video before replacing your original.
