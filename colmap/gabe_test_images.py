from genericpath import exists
import subprocess
import os
import sys
from pathlib import Path

# new imports
import cv2
# Specify the directory where your images are located
directory_path = 'data/outputs\Local_Test/imgs'

# Define a list to store the image file paths
image_list = []

# Use os.listdir to get a list of all files in the directory
all_files = os.listdir(directory_path)

# Make sure only images are selected (The file should only contain images, this is just an extra measure)
for file in all_files:
    if file.lower().endswith(('.png')):
        image_list.append(os.path.join(directory_path, file))

# Now, image_list contains the file paths of all the images in the directory
def is_blurry(image, THRESHOLD):
    ## Convert image to grayscale
    cvimage = cv2.imread(image)
    gray = cv2.cvtColor(cvimage, cv2.COLOR_BGR2GRAY)
    ## run the variance of the laplacian transform to test blurriness
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var < THRESHOLD

print(image_list)
blurry_list = []
trues = 0
for image in image_list:
    blurry_list.append(is_blurry(image, 100))
for blurr in blurry_list:
    if blurr == True:
        trues +=1
    
    print (blurr)
final_percent = trues/(len(blurry_list))
