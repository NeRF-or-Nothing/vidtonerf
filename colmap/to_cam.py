import json
import sys
import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class CameraPoseVisualizer:
    def __init__(self, xlim, ylim, zlim):
        self.fig = plt.figure(figsize=(18, 7))
        self.ax = self.fig.add_subplot(projection='3d')
        self.ax.set_aspect("auto")
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        self.ax.set_zlim(zlim)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('z')

        # Create axis
        axes = [3, 3, 3]
        
        # Create Data
        data = np.ones(axes)
        print(data.shape)
        
        # Control Transparency
        alpha = 0.9
        
        # Control colour
        colors = np.empty(axes + [4], dtype=np.float32)
        
        colors[:] = [1, 0, 0, alpha]  # red
        x,y,z = np.indices((4,4,4),dtype='float32')
        x-= 1.5
        y-= 1.5
        z-= 1.5
        self.ax.voxels(x,y,z,data, facecolors=colors, edgecolors='grey')
        print('initialize camera pose visualizer')

    def extrinsic2pyramid(self, extrinsic, color='r', focal_len_scaled=1, aspect_ratio=0.3):
        vertex_std = np.array([[0, 0, 0, 1],
                               [focal_len_scaled * aspect_ratio, -focal_len_scaled * aspect_ratio, focal_len_scaled, 1],
                               [focal_len_scaled * aspect_ratio, focal_len_scaled * aspect_ratio, focal_len_scaled, 1],
                               [-focal_len_scaled * aspect_ratio, focal_len_scaled * aspect_ratio, focal_len_scaled, 1],
                               [-focal_len_scaled * aspect_ratio, -focal_len_scaled * aspect_ratio, focal_len_scaled, 1]])
        vertex_transformed = vertex_std @ extrinsic.T
        meshes = [[vertex_transformed[0, :-1], vertex_transformed[1][:-1], vertex_transformed[2, :-1]],
                            [vertex_transformed[0, :-1], vertex_transformed[2, :-1], vertex_transformed[3, :-1]],
                            [vertex_transformed[0, :-1], vertex_transformed[3, :-1], vertex_transformed[4, :-1]],
                            [vertex_transformed[0, :-1], vertex_transformed[4, :-1], vertex_transformed[1, :-1]],
                            [vertex_transformed[1, :-1], vertex_transformed[2, :-1], vertex_transformed[3, :-1], vertex_transformed[4, :-1]]]
        self.ax.add_collection3d(
            Poly3DCollection(meshes, facecolors=color, linewidths=0.3, edgecolors=color, alpha=0.15))

    def customize_legend(self, list_label):
        list_handle = []
        for idx, label in enumerate(list_label):
            color = plt.cm.rainbow(idx / len(list_label))
            patch = Patch(color=color, label=label)
            list_handle.append(patch)
        plt.legend(loc='right', bbox_to_anchor=(1.8, 0.5), handles=list_handle)

    def colorbar(self, max_frame_length):
        cmap = mpl.cm.rainbow
        norm = mpl.colors.Normalize(vmin=0, vmax=max_frame_length)
        self.fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), orientation='vertical', label='Frame Number')
    
    def plot_cam(self, cam, color="blue"):
        self.ax.scatter(cam[0],cam[1],cam[2], color= color)


    def show(self):
        print("Displaying Data")
        plt.title('Extrinsic Parameters')
        plt.show()

if __name__ =='__main__':
    print("Starting conversion")
    input_file = sys.argv[1]

    input_str = open(input_file)
    input = json.loads(input_str.read())

    extrins = []
    for f in input["frames"]:
        extrinsic = np.array(f["extrinsic_matrix"])
        extrins+=[ extrinsic ]

    visualizer = CameraPoseVisualizer([-5, 5], [-5, 5], [0, 5])
    cams = []
    for i,e in enumerate(extrins):
        if i%3 == 0:
            color = plt.cm.rainbow(i / len(extrins))
            visualizer.extrinsic2pyramid(e, color)
            primary_point = np.asarray([0,0,-2,1])

            r = e[0:3,0:3]
            t = e[0:3,3]
            c = -r.T @ t
            print("Rotation:\n",r)
            print("Translation:\n",t)
            print("Cam:\n",c)
            print()
            visualizer.plot_cam(e @ primary_point, color)
            secondary_point = np.asarray([0,0,-3,1])
            visualizer.plot_cam(e @ secondary_point, color)


        cams.append(c)
    visualizer.show()






