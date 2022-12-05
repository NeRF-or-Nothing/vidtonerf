import random
import csv
import os
import json
import numpy as np
import io

def gen_cam(filepath):
   #generate 100 sample points
   path = os.path.join(filepath, "images.csv")
   images = []
   for i in range(100, 0, -1):
      image_data = {}
      image_data["Image_Name"] = i

      #quaternion is 4d
      #each coefficient range from -1 to 1
     
      image_data["QW"] = random.uniform(-1,1)
      image_data["QX"] = random.uniform(-1,1)
      image_data["QY"] = random.uniform(-1,1)
      image_data["QZ"] = random.uniform(-1,1)
     
      #adding translation
      image_data["TX"] = random.uniform(-6,6)
      image_data["TY"] = random.uniform(-6,6) 
      image_data["TZ"] = random.uniform(-6,6)

      images.append(image_data)
   
   with open("parsed_data.csv", mode = 'w', newline='') as csv_file:
      csv_file.truncate(0)
      fieldnames = ['Image_Name', 'QW', 'QX', 'QY', 'QZ', 'TX', 'TY', 'TZ']
      writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

      for image in images:
         writer.writerow(image)

def gen_3d(filepath):
   path = os.path.join(filepath, "points3D.txt")
   file = open("points3D.txt", "a")
   points = []
   for i in range(100):
      x = random.uniform(-30,30)
      y = random.uniform(-30,20)
      z = random.uniform(0,40)
      s = str(i) + " "  + str(x) + " "  + str(y) + " " + str(z)
      file.writelines(s)

def get_extrinsics_center(fp: str = "points3D.txt"):
    infile = open(fp, "r")
    lines = infile.readlines()
    point_count = 0

    central_point = np.zeros(3)
    
    for line in lines:
        data = line.split(" ")
        if not data[0].startswith("#"):
            central_point[0] += float(data[1])
            central_point[1] += float(data[2])
            central_point[2] += float(data[3])
            point_count+=1

    central_point /= point_count
    print("Central point: ", central_point)
    return central_point


def get_json_matrices(camera_file, motion_data ):
    center_point = get_extrinsics_center("points3D.txt")
    intrinsic = get_intrinsic("cameras.txt")
    extrinsic = get_extrinsic(center_point, "images.csv")
    intrinsic["frames"] = extrinsic
    return intrinsic

def get_intrinsic(fp: str = "cameras.txt"):
    infile = open(fp, "r")
    lines = infile.readlines()

    for line in lines:
        data = line.split(" ")
        if not data[0].startswith("#"):
            camera = data[1]
            width = int(data[2])
            height = int(data[3])

            fx = float(data[4])
            fy = float(data[5])
            x0 = float(data[6])
            y0 = float(data[7])

    intrinsic = np.array([[fx, 0, x0], 
                          [0, fy, y0],
                          [0, 0, 1]])
    intrinsic_list = intrinsic.tolist() 

    intrinsic = { "vid_width": width,
                  "vid_height": height,
                  "intrinsic_matrix": intrinsic_list
                }

    return intrinsic

def get_extrinsic(center_point, fp: str = "parsed_data.csv"):

    
   # contrains filepath and extrinsic matrix
   filepaths = []
   extrinsic_matrices = []
   with open("parsed_data.csv") as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=",")
      
      next(csv_reader, None)

      for row in csv_reader:
         image_name = str(row[0])
 
         filepaths.append(image_name)

         qw = float(row[1])
         qx = float(row[2])
         qy = float(row[3])
         qz = float(row[4])

         tx = float(row[5])
         ty = float(row[6])
         tz = float(row[7])
      
         # find extrinsic matrix
         T = np.array([tx, ty, tz])
         r = quaternion_rotation_matrix(qw, qx, qy, qz)  # rotational matrix


         extrinsic = np.zeros((4,4))
         extrinsic[0:3,0:3] = r
         extrinsic[0:3,3] = T

         #T is not the position of the camera
         #r_t = r.transpose()
         #camera = -r_t @T
         extrinsic[3][3] = 1
         c2w = np.linalg.inv(extrinsic)

         # convert from OPENCV to OPENGL coordinates
         conversion = np.array([[1,0,0,0],
                                 [0,-1,0,0],
                                 [0,0,-1,0],
                                 [0,0,0,1]])
         # flips y and z coords
         c2w =  c2w @ conversion

         extrinsic_matrices.append(c2w)
         
         # Center extrinsics around center point:
         #extrinsic[0:3,3] += center_point
  
   # stack all extrinsic to perform faster transformations to the whole stack
   extrinsic_matrices = np.stack(extrinsic_matrices,axis=0)
   print(extrinsic_matrices.shape)
   avg_y_axis = np.sum(extrinsic_matrices[:,0:3,1], axis=0)
   avg_y_axis = avg_y_axis/np.linalg.norm(avg_y_axis)
   print("Consensus Y axis: ",avg_y_axis)

   # Find a matrix to rotate the average y axis with the y-axis unit vector thus aligning every extrinsic to point in the same direction
   Rot = np.zeros((4,4))
   Rot[0:3,0:3] = rotation_matrix_from_vectors(avg_y_axis,np.asarray([0,0,1]))
   Rot[-1,-1] = 1
   Rot = np.expand_dims(Rot,axis=0)

   # Rotate Extrinsic to all face up
   extrinsic_matrices = Rot @ extrinsic_matrices

   # Adjust extrinsic to center around the central point
   #center_point = np.average(extrinsic_matrices[:,0:3,3],axis=0)
   print(center_point.shape)
   print("center point ",center_point)
   extrinsic_matrices[:,0:3,3] -= center_point

   # Z offset assuming cameras are never below the object
   extrinsic_matrices[:,2,3] -= min(extrinsic_matrices[:,2,3].min(),0)

   # Normalize extrinsic transformation to remain within bounding box
   translation_magnitudes = np.linalg.norm(extrinsic_matrices[:,0:3,3],axis=1)
   avg_translation_magnitude = np.average(translation_magnitudes)
   print("Translation mag: ",avg_translation_magnitude)
   extrinsic_matrices[:,0:3,3] /= avg_translation_magnitude

   # scale back up TODO: make dynamic
   extrinsic_matrices[:,0:3,3] *= 4

   print("Max ",extrinsic_matrices[:,0:3,3].max())
   print("Min ",extrinsic_matrices[:,0:3,3].min())
   print("avg ",np.average(extrinsic_matrices[:,0:3,3]))

   # Convert to json
   frames = []
   for extrin, file_path in zip(extrinsic_matrices,filepaths):
      extrinsic_list = extrin.tolist()        # convert to list for json

      img_frame = { "file_path": file_path,
                        "extrinsic_matrix": extrinsic_list}

      frames.append(img_frame)

   return frames
 
def rotation_matrix_from_vectors(vec1, vec2):
   """ Find the rotation matrix that aligns vec1 to vec2
   :param vec1: A 3d "source" vector
   :param vec2: A 3d "destination" vector
   :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
   """
   a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
   v = np.cross(a, b)
   c = np.dot(a, b)
   s = np.linalg.norm(v)
   kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
   rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
   return rotation_matrix

def quaternion_rotation_matrix(qw, qx, qy, qz) -> np.ndarray:
    # w   x   y   z
    """
    Convert a quaternion into a full three-dimensional rotation matrix.

    Parameters
    ----------
    qw, qx, qy, qz : float
        A 4 element array representing the quaternion (qw,qx,qy,qz)

    Returns
    -------
    rotation_matrix : np.ndarray
        A 3x3 element matrix representing the full 3D rotation matrix.
        This rotation matrix converts a point in the local reference
        frame to a point in the global reference frame.
    """

    # First row of the rotation matrix
    r00 = 1 - 2 * qy**2 - 2 * qz**2
    r01 = 2 * qx * qy - 2 * qz * qw
    r02 = 2 * qx * qz + 2 * qy * qw

    # Second row of the rotation matrix
    r10 = 2 * qx * qy + 2 * qz * qw
    r11 = 1 - 2 * qx**2 - 2 * qz**2
    r12 = 2 * qy * qz - 2 * qx * qw

    # Third row of the rotation matrix
    r20 = 2 * qx * qz - 2 * qy * qw
    r21 = 2 * qy * qz + 2 * qx * qw
    r22 = 1 - 2 * qx**2 - 2 * qy**2

    # 3x3 rotation matrix
    rotation_matrix = np.array([[r00, r01, r02],
                                [r10, r11, r12],
                                [r20, r21, r22]])
    # np.set_printoptions(threshold=sys.maxsize)
    return rotation_matrix


if __name__ == '__main__':
   output_path = os.getcwd() + "\sfm_test"
   
   initial_motion_path = os.path.join(output_path,"images.txt")
   camera_stats_path = os.path.join(output_path,"cameras.txt")
   parsed_motion_path = os.path.join(output_path,"parsed_data.csv")
   threed_path = os.path.join(output_path,"points3D.txt")

   gen_3d(threed_path)
   gen_cam(parsed_motion_path)
   
   
   motion_data = get_json_matrices(camera_stats_path, parsed_motion_path)

   motion_data["id"] = id
   '''
    # Save copy of motion data
   with open("transforms_data.json", 'w') as outfile:
      outfile.write(json.dumps(motion_data, indent=4))
   '''
  


   
 
