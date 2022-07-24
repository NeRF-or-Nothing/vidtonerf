import subprocess
import os
import sys

#Usage: python ColmapRunner.py --flags
#Flags: --output_folder "path"   ==> Directory to where colmap will put its output.
#                                  > Defaults to the folder where this script is
#
#       --name "name"            ==> Name of the folder to be created to store the data for this instance
#                                  > of colmap.
#                                  > Defaults to "colmap_output"
#
#       --colmap_exe_path "path" ==> Path to the colmap executeable.
#                                  > Defaults to looking for COLMAP.bat in a folder called COLMAP in the 
#                                  > folder this script is in
#
#       --image_path "path"      ==> Path to the folder containing the images for COLMAP's input
#                                  > Defailts to looking for a folder called "Images" in the folder 
#                                  > this script is in

def run_colmap(instance_name, output_path, colmap_path, images_path):
    ### Create a new folder to store our data
      # Add a / to the path if there isn't one
    if not output_path.endswith(("\\", "/")) and not instance_name.startswith(("\\", "/")):
        output_path = output_path + "/"
    instance_path = output_path + instance_name
    os.mkdir(instance_path)

    #Creating a new database for colmap
    database_path = instance_path + "/database.db"
    subprocess.call([colmap_path, "database_creator", "--database_path", database_path])

    #Feature extracting
    subprocess.call([colmap_path, "feature_extractor", "--database_path", database_path, "--image_path", images_path])

    #Feature matching
    subprocess.call([colmap_path, "exhaustive_matcher", "--database_path", database_path])

    #Generating model
    subprocess.call([colmap_path, "mapper", "--database_path", database_path, "--image_path", images_path, "--output_path", instance_path])

    #Getting model as text
    subprocess.call([colmap_path, "model_converter", "--input_path", instance_path + r"\0", "--output_path", instance_path, "--output_type", "TXT"])

    return 0;


if __name__ == '__main__':
    #Default flags
    instance_name = "colmap_output"
    output_path = "./"
    colmap_path = r".\COLMAP\COLMAP.bat"
    images_path = r".\Images"

    #Parse flags
    #Flag format up top
    for i in range (len(sys.argv)):
        if i == 0:
            continue
        if sys.argv[i].startswith("--"):
            match sys.argv[i]:
                case "--output_folder":
                    output_path = sys.argv[i+1]
                case "--name":
                    instance_name = sys.argv[i+1]
                case "--colmap_exe_path":
                    colmap_path = sys.argv[i+1]
                case "--image_path":
                    images_path = sys.argv[i+1]
                case _:
                    print("Error: Unrecognized flag", sys.argv[i])
                    quit()
    #Run COLMAP :)
    if run_colmap(instance_name, output_path, colmap_path, images_path) == 0:
        print("COLMAP run successfully.")
    else:
        print("ERROR: There was a problem running COLMAP")