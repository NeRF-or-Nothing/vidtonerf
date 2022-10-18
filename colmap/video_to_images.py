from genericpath import exists
import subprocess
import os
import sys
from pathlib import Path

# new imports
import cv2
from random import sample
#Usage: python video_to_images.py --flags
#Flags: --ffmpeg_exe_path "path" ==> Path to the ffmpeg executeable.
#                                  > Defaults to looking for ffmpeg.exe in the folder this script is in.
#
#       --wanted_frames "uint"   ==> Number of frames we want to use
#                                  > If total frames < wanted_frames, we default to total frames
#                                  > Defaults to 200.
#
#       --name "name"            ==> Name of the folder to be created to store the data for this instance
#                                  > of ffmpeg.
#                                  > Defaults to "ffmpeg_output"
#
#       --output_folder "path"   ==> Directory to where ffmpeg will put its output.
#                                  > Defaults to the folder where this script is
#
#       --video_path "path"      ==> Path to the video to be converted into its composite images.
#                                  > Defaults to looking for "video.mp4" in the folder this script
#                                  > is in.



#split_video_into_frames function:
#
#creates a new folder called instance_name in output_path and fills it with the frames
#    of the video at video_path. Samples wanted_frames amount of frames,
#    or 200 frames by default
#
#returns a status code - 
#    0 = Success
#    1 = Unspecified error
#    2 = FileExistsError; happens when you try to create data in an already existing folder
#    3 = FileNotFoundError; happens when you try to use an output folder that does not exist

def split_video_into_frames(video_path, output_path, max_frames=200):
   # Create output folder
    Path(f"{output_path}").mkdir(parents=True, exist_ok=True)


    ## determine video length:
    # TODO: Check video type to ensure it is supported
    vidcap = cv2.VideoCapture(video_path )
    frame_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_count = int(frame_count)

    ## sample up to max frame count
    sample_count = min(frame_count,max_frames)

    #print(f"frames = {frame_count}")

    success, image = vidcap.read()
    img_height = image.shape[0]
    img_width = image.shape[1]
    needs_adjust = False ## determines if we need to adjust
    aspect_ratio = img_height / img_width
    #print (f"aspect ratio: {aspect_ratio}")
    #print (f"img_width: {img_width}")
    #print (f"img_height: {img_height}")
    ## adjust as necessary
    MAX_WIDTH = 200 
    MAX_HEIGHT = 200

    ## for resizing images
    # TODO: Fix image resizing to preserve aspect ratio
    if (img_height > MAX_HEIGHT):
      scaler = MAX_HEIGHT / img_height
      img_height = (int) (img_height * scaler)
      needs_adjust = True

    if (img_width > MAX_WIDTH):
      scaler = MAX_WIDTH / img_width
      img_width = (int) (scaler * img_width)
      needs_adjust = True
    
    ## applying aspect ratio
    if (aspect_ratio > 1):
      img_width = (int) (img_width / aspect_ratio)
    else:
      img_height = (int) (img_height * aspect_ratio)

    #print(f"new img height: {img_height}")
    #print(f"new img width: {img_width}")
    dimensions = (img_width, img_height)

    count = 0
    next_up = 0 # used for iterating through the sorted sample images

    ## finding which images we will randomly take
    image_indexes = [i for i in range(frame_count)]
    chosen_list = sample(image_indexes, sample_count)
    chosen_list = sorted(chosen_list)
    print(chosen_list)
    while success:
      if (next_up == len(chosen_list)):
        break
      if (chosen_list[next_up] == count):
        next_up += 1
        if (needs_adjust == True):
          image = cv2.resize(image, dimensions, interpolation=cv2.INTER_LANCZOS4)
        cv2.imwrite(f"{output_path}/img_{next_up}.png", image)  
        print('Saved image ', next_up)
      success, image = vidcap.read()
      count += 1
    vidcap.release()

    #Sucess, return 0
    ## can return img_width, img_height, and wanted_frames
    return 0

def test():
  instance_name = "test"
  output_path = "test_out"
  ffmpeg_path = ""
  video_path = "landscape_video" # change to whatever vid you want
  wanted_frames = 200
  split_video_into_frames(instance_name, output_path, ffmpeg_path, video_path, wanted_frames)

if __name__ == '__main__':
    #Default flags
    instance_name = "ffmpeg_output"
    output_path = "./"
    ffmpeg_path = r".\ffmpeg.exe"
    video_path = r".\video.mp4"
    wanted_frames = 24

    #Parse flags
    #Flag format up top
    """
    for i in range (len(sys.argv)):
        if i == 0:
            continue
        if sys.argv[i].startswith("--"):
            match sys.argv[i]:
                case "--output_folder":
                    output_path = sys.argv[i+1]
                case "--name":
                    instance_name = sys.argv[i+1]
                case "--ffmpeg_exe_path":
                    ffmpeg_path = sys.argv[i+1]
                case "--video_path":
                    video_path = sys.argv[i+1]
                case "--fps":
                    fps = sys.argv[i+1]
                case _:
                    print("ERROR: Unrecognized flag", sys.argv[i])
                    quit()"""
    
    #Calling split_video_into_frames
    status = split_video_into_frames(instance_name, output_path, ffmpeg_path, video_path, wanted_frames=200)
    if status == 0:
        print("ffmpeg ran successfully.")
    elif status == 1:
        print("ERROR: There was an unknown error running ffmpeg")
    elif status == 2:
        print(f"ERROR: ffmpeg - file {output_path}/{instance_name} already exists.")
    elif status == 3:
        print(f"ERROR: ffmpeg - file {output_path} could not be found.")