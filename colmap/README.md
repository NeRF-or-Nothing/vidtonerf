### COLMAP
COLMAP is a general-purpose Structure-from-Motion (SfM) and Multi-View Stereo (MVS) pipeline
that is used for estimating three-dimensional structures from two-dimensional image
sequences. This project will be using the image camera data output from COLMAP and
implementing it to the NeRF.

Currently, this project will run COLMAP from command line using python script. Using the generate output of each images, process the data using colmap2data.py to extract the quaternion and transpose vector. Finally, feed the data to data2matrix.py that converts the data to an extrinsic matrix to be used by NeRF.

### Data Processing

Image list with two lines of data per image:
IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME\
POINTS2D[ ] as (X, Y, POINT3D_ID)

Quaternion: QW, QX, QY, QZ\
Transpose Vector: TX, TY, TZ

-r^t * T = coordinate of project/camera center
- r^t = inverse/transpose of the 3x3 rotation matrix composed from the quaternion
- T = translation vector

The quaternion elements will first be converted to a rotational matrix. Then, the coordinate of the images' camera center can be computed by taking the inverse of this rotational matrix multiplied by the translation vector. This is essentially the extrinsic matrix that describes the camera's location in the world, and what direction it's pointing.

Quaternion can also be used to calculate the Euler angles which contains the roll, pitch, and yaw of the three rotational axes.
- Roll is rotation around x in radians (counterclockwise)
- Pitch is rotation around y in radians (counterclockwise)
- Yaw is rotation around z in radians (counterclockwise)

### Good Data Collection Tips
- Try to take pictures/videos in a clean background that is not messy
- Take structure in an environment that has opposing color to the structure itself
- Take a decent amount of pictures that covers a wide range of position
- Try to take images with the same angles among an axis


### Reference for Additional Research
- COLMAP Installation\
https://colmap.github.io/install.html
- COLMAP Data Output Format\
https://colmap.github.io/format.html
- Quaternion to Rotational Matrix\
https://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToMatrix/index.htm
- Quaternion to Euler Angle\
https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
- Extrinsic Matrix\
https://ksimek.github.io/2012/08/22/extrinsic/
- GAN-based Neural Radiance Field
https://www.researchgate.net/publication/350484366_GNeRF_GAN-based_Neural_Radiance_Field_without_Posed_Camera


