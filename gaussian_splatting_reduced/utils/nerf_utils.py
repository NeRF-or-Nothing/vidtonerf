from plyfile import PlyData
from io import BytesIO
from sys import maxsize

import numpy as np

import json
import sys


def convert_transforms_to_gaussian(transforms):
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
                "transform_matrix": [[r11, r12, r13, t1], [r21, r22, r23, t2], [r31, r32, r33, t3], [0, 0, 0, 1]]
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
    transforms["camera_angle_x"] = fovx
    transforms["camera_angle_y"] = fovy

    for i, fr in enumerate(transforms["frames"]):
        fr["transform_matrix"] = fr.pop("extrinsic_matrix")

    return transforms


def convert_transforms_to_tensorf(transforms):
    '''
    TODO: If needed
    '''
    pass


def convert_ply_to_splat(ply_file_path, num_splats, verbose=False):
    """
    Convert a .ply file to a "compressed" .splat file for use in the
    frontend renderer. 1M splats is roughly 50MB compressed.

    Args:
        ply_file_path (_type_): Path to the .ply file to convert
        num_splats (_type_): Number of splats to convert. Defaults to maxsize.
        verbose (bool, optional): Defaults to False.
    """
    plydata = PlyData.read(ply_file_path)
    vert = plydata["vertex"]
    sorted_indices = np.argsort(
        -np.exp(vert["scale_0"] + vert["scale_1"] + vert["scale_2"])
        / (1 + np.exp(-vert["opacity"]))
    )
    buffer = BytesIO()
    num_converted = 0
    for idx in sorted_indices:
        v = plydata["vertex"][idx]
        position = np.array([v["x"], v["y"], v["z"]], dtype=np.float32)
        scales = np.exp(
            np.array(
                [v["scale_0"], v["scale_1"], v["scale_2"]],
                dtype=np.float32,
            )
        )
        rot = np.array(
            [v["rot_0"], v["rot_1"], v["rot_2"], v["rot_3"]],
            dtype=np.float32,
        )
        SH_C0 = 0.28209479177387814
        color = np.array(
            [
                0.5 + SH_C0 * v["f_dc_0"],
                0.5 + SH_C0 * v["f_dc_1"],
                0.5 + SH_C0 * v["f_dc_2"],
                1 / (1 + np.exp(-v["opacity"])),
            ]
        )
        buffer.write(position.tobytes())
        buffer.write(scales.tobytes())
        buffer.write((color * 255).clip(0, 255).astype(np.uint8).tobytes())
        buffer.write(
            ((rot / np.linalg.norm(rot)) * 128 + 128)
            .clip(0, 255)
            .astype(np.uint8)
            .tobytes()
        )

        if verbose and num_converted % int(num_splats / 100) == 0:
            print(f"Converted {num_converted} splats", end="\r")

        num_converted += 1
        if num_splats != 0 and num_converted == num_splats:
            break

    print(f"Converted {num_converted} splats", end="\r")
    return buffer.getvalue()


if __name__ == "__main__":
    path = sys.argv[1]
    data = convert_transforms_to_gaussian(json.load(open(path, 'r')))
    with open(path, 'w') as f:
        json.dump(data, f)
