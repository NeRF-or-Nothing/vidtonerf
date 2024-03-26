import json
import sys

from cv2 import inpaint

if __name__ =='__main__':
    print("Starting conversion")
    input_file = sys.argv[1]

    input_str = open(input_file)
    input = json.loads(input_str.read())
    input["vid_width"] = 800
    input["vid_height"] = 800
    focal = input["camera_angle_x"]
    input["intrinsic_matrix"] = [[focal, 0, 400],
                                [0, focal, 0, 400],
                                [0,0,1]]
    for f in input["frames"]:
        f["extrinsic_matrix"] = f["transform_matrix"]

    print(json.dumps(input))

    with open("new_"+input_file, "w") as outfile:
        outfile.write(json.dumps(input,indent=4))




