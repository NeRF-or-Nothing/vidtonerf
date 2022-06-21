import subprocess
import os
import shutil

#Create a new folder to store our data
output_path = r"C:\Users\digioa\Documents\School\RCOS\COLMAP/"
project_name = "test"
project_path = output_path + project_name
os.mkdir(project_path)

#Path to colmap executable
colmap_path = r"C:\Users\digioa\Documents\School\RCOS\COLMAP\COLMAP-3.7-windows-no-cuda\COLMAP.bat"

#Path to Images
images_path = r"C:\Users\digioa\Documents\School\RCOS\COLMAP\Images"

#Creating a new database for our use
database_path = project_path + "/database.db"
subprocess.call([colmap_path, "database_creator", "--database_path", database_path])

#Feature extracting
subprocess.call([colmap_path, "feature_extractor", "--database_path", database_path, "--image_path", images_path])

#Feature matching
subprocess.call([colmap_path, "exhaustive_matcher", "--database_path", database_path])

#Generating model
subprocess.call([colmap_path, "mapper", "--database_path", database_path, "--image_path", images_path, "--output_path", project_path])

#Getting model as text
subprocess.call([colmap_path, "model_converter", "--input_path", project_path + r"\0", "--output_path", project_path, "--output_type", "TXT"])