import json
import numpy as np

if __name__ == "__main__":
    path = "test_data/transforms_train.json"
    with open(path, 'r') as file:
        transforms = json.load(file)
    # print(transforms)
    intrinsic = np.array(transforms["intrinsic_matrix"])
    width = transforms["vid_width"]
    height = transforms["vid_height"]
    fovx = 2 * np.tanh(width / (2 * intrinsic[0,    0]))
    fovy = 2 * np.tanh(height / (2 * intrinsic[1, 1]))
    print("FovX: ", fovx)
    print("FovY: ", fovy)
    transforms["camera_angle_x"] = fovx
    transforms["camera_angle_y"] = fovy

    for i, fr in enumerate(transforms["frames"]):
        print("Frame ", fr)
        fr["transform_matrix"] = fr.pop("extrinsic_matrix")

    with open(path, 'w') as file:
        file.write(json.dumps(transforms, indent=4))
