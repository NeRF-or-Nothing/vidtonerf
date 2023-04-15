import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import json

def counter(extrinsics, intrinsic, lims):

    xlim = lims[0]
    ylim = lims[1]
    zlim = lims[2]

    p_0 = np.array([
        [xlim[0], 0, 0],
        [xlim[1], 0, 0],
        [0, ylim[0], 0],
        [0, ylim[1], 0],
        [0, 0, zlim[0]],
        [0, 0, zlim[1]]
    ])

    n = np.array([
        [-1, 0, 0],
        [1, 0, 0],
        [0, -1, 0],
        [0, 1, 0],
        [0, 0, -1],
        [0, 0, 1]
    ])    

    count_tot = 0
    for matrix in extrinsics:

        l_0 = matrix[:, 3][:3]
        l = np.linalg.inv(intrinsic) @ np.array([0, 0, 1])
        l = np.append(l, 1)
        l = matrix @ l
        l = l[:3]
        
        count_int = 0
        for i in range(0, 6):

            d = ((p_0[i] - l_0).T @ n[i])/(l.T @ n[i])
            p = l_0 + l*d

            if i == 1 or i == 2:

                if (p[1] > ylim[0] and p[1] < ylim[1]) and (p[2] > zlim[0] and p[2] < zlim[1]):

                    count_int += 1

            if i == 3 or i == 4:

                if (p[0] > xlim[0] and p[0] < xlim[1]) and (p[2] > zlim[0] and p[2] < zlim[1]):
                    
                    count_int += 1

            if i == 5 or i == 6:

                if (p[0] > xlim[0] and p[0] < xlim[1]) and (p[1] > ylim[0] and p[1] < ylim[1]):

                    count_int += 1
        
        if count_int > 0:

            count_tot += 1

    return count_tot

if __name__ == '__main__':

    transforms_data = json.load(open('./data/outputs/Local_Test/transforms_data.json'))
    extrinsics = np.array([np.array(frame['extrinsic_matrix']) for frame in transforms_data['frames']])
    intrinsic = transforms_data['intrinsic_matrix']

    xlim = [-1, 1]
    ylim = [-1, 1]
    zlim = [-1, 1]

    lims = np.array([xlim, ylim, zlim])

    print(counter(extrinsics, intrinsic, lims)/len(extrinsics))

    #Plotting camera path
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(projection='3d')
    ax.set_xlim([-5, 5])
    ax.set_ylim([-5, 5])
    ax.set_zlim([-5, 5])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    focal_len_scaled = 1
    aspect_ratio = 0.3

    for matrix in extrinsics:

        vertex_camera = np.array([[0, 0, 0, 1],
                                [focal_len_scaled * aspect_ratio, -focal_len_scaled * aspect_ratio, focal_len_scaled, 1],
                                [focal_len_scaled * aspect_ratio, focal_len_scaled * aspect_ratio, focal_len_scaled, 1],
                                [-focal_len_scaled * aspect_ratio, focal_len_scaled * aspect_ratio, focal_len_scaled, 1],
                                [-focal_len_scaled * aspect_ratio, -focal_len_scaled * aspect_ratio, focal_len_scaled, 1]])

        vertex_transformed = vertex_camera @ matrix.T

        meshes = [[vertex_transformed[0, :-1], vertex_transformed[1][:-1], vertex_transformed[2, :-1]],
                                [vertex_transformed[0, :-1], vertex_transformed[2, :-1], vertex_transformed[3, :-1]],
                                [vertex_transformed[0, :-1], vertex_transformed[3, :-1], vertex_transformed[4, :-1]],
                                [vertex_transformed[0, :-1], vertex_transformed[4, :-1], vertex_transformed[1, :-1]],
                                [vertex_transformed[1, :-1], vertex_transformed[2, :-1], vertex_transformed[3, :-1], vertex_transformed[4, :-1]]]
        ax.add_collection3d(Poly3DCollection(meshes, linewidths=0.3, alpha=0.15, color = 'red'))

        camera_loc = np.array([0, 0, 0, 1])
        vertex_transformed = camera_loc @ matrix.T

        ax.plot([vertex_transformed[0], 0.5*vertex_transformed[0]], [vertex_transformed[1], 0.5*vertex_transformed[1]], [vertex_transformed[2], 0.5*vertex_transformed[2]], c = 'black', alpha = 0.1)

    box = np.array([
        [[xlim[0], ylim[0], zlim[0]], [xlim[1], ylim[0], zlim[0]], [xlim[1], ylim[0], zlim[1]], [xlim[0], ylim[0], zlim[1]]], 
        [[xlim[0], ylim[0], zlim[0]], [xlim[0], ylim[1], zlim[0]], [zlim[0], ylim[1], zlim[1]], [zlim[0], ylim[0], zlim[1]]],
        [[xlim[0], ylim[1], zlim[0]], [xlim[0], ylim[1], zlim[1]], [xlim[1], ylim[1], zlim[1]], [xlim[1], ylim[1], zlim[0]]],
        [[xlim[1], ylim[0], ylim[0]], [xlim[1], ylim[1], zlim[0]], [xlim[1], ylim[1], zlim[1]], [xlim[1], ylim[0], zlim[1]]],
        [[xlim[0], ylim[0], zlim[0]], [xlim[1], ylim[0], zlim[0]], [xlim[1], ylim[1], zlim[0]], [xlim[0], ylim[1], zlim[0]]],
        [[xlim[0], ylim[0], zlim[1]], [xlim[1], ylim[0], zlim[1]], [xlim[1], ylim[1], zlim[1]], [xlim[0], ylim[1], zlim[1]]]
        ])
    ax.add_collection3d(Poly3DCollection(box, alpha = 0.5))

    C = extrinsics[:, :, 3]
    C = np.moveaxis(C, 0, 1)
    ax.scatter(0, 0, 0, c = 'black', marker = '+', )
    ax.scatter(C[0], C[1], C[2], c = np.arange(len(C[0])))

    plt.show()