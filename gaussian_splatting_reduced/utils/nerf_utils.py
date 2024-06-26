import json
import numpy as np\

def convert_transforms_to_gaussian(transforms ):
    '''
    Utility function to convert the transforms file from the format TensoRF uses to
    the format used by the gaussian splatting code. See online resources for more 
    camera/world space transformation details.

    The format we use for TensoRF is:
    {
        "intrinsic_matrix": [[focal_x, 0, center_x], [0, focal_y, center_y], [0, 0, 1]],
        "vid_width": width,
        "vid_height": height,
        "frames": [
            {
                "file_path": "path/to/image",
                "extrinsic_matrix": [[r11, r12, r13, t1], [r21, r22, r23, t2], [r31, r32, r33, t3], [0, 0, 0, 1]]
            },
            ...
        ]
    }
    The format used by the gaussian splatting code is:
    {
        "camera_angle_x": fov_x,
        "camera_angle_y": fov_y,
        "frames": [
            {
                "file_path": "path/to/image",
                "transform_matrix": [[r11, r12, r13, t1], 
                                    [r21, r22, r23, t2], 
                                    [r31, r32, r33, t3], 
                                    [0, 0, 0, 1]]
            },
            ...
        ]
    }
    '''
    intrinsic = np.array(transforms["intrinsic_matrix"])
    width = transforms["vid_width"]
    height = transforms["vid_height"]
    fovx = 2 * np.tanh(width / (2 * intrinsic[0,    0]))
    fovy = 2 * np.tanh(height / (2 * intrinsic[1, 1]))
    # print(transforms)
    # print("FovX: ", fovx)
    # print("FovY: ", fovy)
    transforms["camera_angle_x"] = fovx
    transforms["camera_angle_y"] = fovy

    for i, fr in enumerate(transforms["frames"]):
        # print("Frame ", fr)
        fr["transform_matrix"] = fr.pop("extrinsic_matrix")

    return transforms

def convert_transforms_to_tensorf(transforms):
    '''
    HG
    '''

if __name__ == "__main__":
    path = "data/nerf_data/transforms_train.json"
    convert_transforms(json.load(open(path, 'r')))