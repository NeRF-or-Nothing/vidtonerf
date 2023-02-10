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
  ## determines whether image is blurry or not.
  # uses the variance of a laplacian transform to check for edges and returns true
  # if the variance is less than the threshold and the video is determined to be blurry
  def is_blurry(image, THRESHOLD):
    ## Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ## run the variance of the laplacian transform to test blurriness
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var < THRESHOLD

  ## determines amount of blurriness
  # see IS_BLURRY for more information
  def blurriness(image):
    ## Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ## run the variance of the laplacian transform to test blurriness
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var

  # Create output folder
  Path(f"{output_path}").mkdir(parents=True, exist_ok=True)

  ## determine video length:
  # TODO: Check video type to ensure it is supported
  vidcap = cv2.VideoCapture(video_path )
  frame_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
  frame_count = int(frame_count)

  ## sample up to max frame count
  sample_count = min(frame_count,max_frames)
  print("SAMPLE COUNT:", sample_count)

  #print(f"frames = {frame_count}")

  success, image = vidcap.read()
  img_height = image.shape[0]
  img_width = image.shape[1]

  ## Rank all images based off bluriness
  blur_list = []
  ## check blurriness of all images and sort to caluculate threshold
  while success:
    image_blur = blurriness(image)
    blur_list.append(image_blur)
    success, image = vidcap.read()

  vidcap.release()
  sorted_list = sorted(blur_list)
  ## we want the remaining best images
  ## e.g, if we want 75 images out of 100, threshold should be 25th image
  threshold_img = len(blur_list) - sample_count
  THRESHOLD = sorted_list[threshold_img]

  ## checks number of images within the threshold
  count_good_img = 0
  for i in blur_list:
    if i >= THRESHOLD:
      count_good_img += 1

  ## account for not enough images in threshold so that we return the exact number of images
  if count_good_img > sample_count:
    for i in range(count_good_img - sample_count):
      for val in blur_list:
        if val >= THRESHOLD:
          val = 0
          break
       

  ## If this threshold is too low, completely reject video 
  avg_threshold = (sorted_list[-1] + THRESHOLD)/2
  if avg_threshold < 100:
    # ERROR: Video is too blurry. Please try again.
    return 4
  

  needs_adjust = False ## determines if we need to adjust
  aspect_ratio = img_height / img_width
  #print (f"aspect ratio: {aspect_ratio}")
  #print (f"img_width: {img_width}")
  #print (f"img_height: {img_height}")
  ## adjust as necessaryx 
  MAX_WIDTH = 200 
  MAX_HEIGHT = 200

  ## for resizing images
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

  ## write to the folder the images we want
  vidcap = cv2.VideoCapture(video_path)
  success, image = vidcap.read()
  while success:
    if (blur_list[count] >= THRESHOLD):
      if (needs_adjust == True):
        image = cv2.resize(image, dimensions, interpolation=cv2.INTER_LANCZOS4)
      cv2.imwrite(f"{output_path}/img_{count}.png", image)  
      print('Saved image ', count)
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
    elif status == 4:
        print("ERROR: Video is too blurry. Please try again.")