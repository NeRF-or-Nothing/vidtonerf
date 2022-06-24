"""
-r^t * T = Coordinate of project/camera center:
r^t = inverse/transpose of the 3x3 rotation matrix composed from the quaternion
T = translation vector
python3 matrix.py output.csv >out.txt
(Annie)
"""

import sys
import os
import csv
import math
import numpy as np
from pathlib import Path
import PIL
from PIL import Image

# https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
def euler_from_quaternion(x, y, z, w):
    """
    Convert a quaternion into euler angles (roll, pitch, yaw)
    roll is rotation around x in radians (counterclockwise)
    pitch is rotation around y in radians (counterclockwise)
    yaw is rotation around z in radians (counterclockwise)
    """
    # roll (x-axis rotation)
    sinr_cosp = +2.0 * (w * x + y * z)
    cosr_cosp = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(sinr_cosp, cosr_cosp)

    # pitch (y-axis rotation)
    sinp  = +2.0 * (w * y - z * x)
    sinp  = +1.0 if sinp  > +1.0 else sinp
    sinp  = -1.0 if sinp  < -1.0 else sinp
    pitch_y = math.asin(sinp)

    # yaw (x-axis rotation)
    siny_cosp  = +2.0 * (w * z + x * y)
    cosy_cosp  = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(siny_cosp, cosy_cosp)

    return roll_x, pitch_y, yaw_z  # in radians

# https://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToMatrix/index.htm
def quaternion_rotation_matrix(qw, qx, qy, qz):
                              # w   x   y   z
    """
    Covert a quaternion into a full three-dimensional rotation matrix.

    Input
    :param Q: A 4 element array representing the quaternion (q0,q1,q2,q3)

    Output
    :return: A 3x3 element matrix representing the full 3D rotation matrix.
             This rotation matrix converts a point in the local reference
             frame to a point in the global reference frame.
    """

    # First row of the rotation matrix
    r00 = 1 - 2*qy**2 - 2*qz**2
    r01 = 2*qx*qy - 2*qz*qw
    r02 = 2*qx*qz + 2*qy*qw

    # Second row of the rotation matrix
    r10 = 2*qx*qy + 2*qz*qw
    r11 = 1 - 2*qx**2 - 2*qz**2
    r12 = 2*qy*qz - 2*qx*qw

    # Third row of the rotation matrix
    r20 = 2*qx*qz - 2*qy*qw
    r21 = 2*qy*qz + 2*qx*qw
    r22 = 1 - 2*qx**2 - 2*qy**2

    # 3x3 rotation matrix
    rotation_matrix = np.array([[r00, r01, r02],
                                [r10, r11, r12],
                                [r20, r21, r22]])
    #np.set_printoptions(threshold=sys.maxsize)
    return rotation_matrix


def main():
    # check for input argument
    if len(sys.argv) != 2:
        print("Invalid usage. Correct usage: python3 matrix.py \"output.csv\"")
        sys.exit()

    # opening input file
    with open(sys.argv[1]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row = next(csv_reader) # start with second line
        for row in csv_reader:
            image_name = str(row[0])

            qw = float(row[1])
            qx = float(row[2])
            qy = float(row[3])
            qz = float(row[4])

            tx = float(row[5])
            ty = float(row[6])
            tz = float(row[7])

            # find extrinsic matrix
            T = np.array([tx, ty, tz])
            rotation_matrix = quaternion_rotation_matrix(qw, qx, qy, qz)
            projection_center = -rotation_matrix * T

            # image resolution
            dir1 = "//mnt//c//Users//xuj18//Dropbox//NeRF//pytesting//images//"
            path = dir1 + image_name

            img = PIL.Image.open(path)
            wid, hgt = img.size

            #transposed = np.linalg.inv(rotation_matrix) * T
            print(image_name + " ("+str(wid) + "x" + str(hgt)+")")
            print(projection_center)
            print("\n")

if __name__ == "__main__":
    main()

