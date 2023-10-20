import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import json

def counter(extrinsics, intrinsic, lims):
    #function takes an input of extrinsic matrices, the intrinsic matrice (not used currently), and the limits of the bounding box as a numpy array size 3 x 2.
    #bounding box exists as measurment of how centered the photos are, and thus, whether or not the user needs to retry with a different video.

    xlim = lims[0]
    ylim = lims[1]
    zlim = lims[2]

    #points on each side of bounding box
    p_0 = np.array([
        [xlim[0], 0, 0],
        [xlim[1], 0, 0],
        [0, ylim[0], 0],
        [0, ylim[1], 0],
        [0, 0, zlim[0]],
        [0, 0, zlim[1]]
    ])

    #normal vectors to each side of bounding box
    n = np.array([
        [-1, 0, 0],
        [1, 0, 0],
        [0, -1, 0],
        [0, 1, 0],
        [0, 0, -1],
        [0, 0, 1]
    ])    

    count_tot = 0
    points = []
    for matrix in extrinsics:

        #compute direction of each camera using a centered vector
        l = matrix @ np.array([0, 0, -1, 1])
        l = l[:3]
        l_0 = matrix[:, 3][:3]
        
        #finding intersection with each side of bounding box
        count_int = 0
        for i in range(0, 6):

            d = ((p_0[i] - l_0).T @ n[i])/(l.T @ n[i])
            p = l_0 + l*d

            #planes fixed in x 
            if (i == 0) or (i == 1):

                if (p[1] > ylim[0] and p[1] < ylim[1]) and (p[2] > zlim[0] and p[2] < zlim[1]):

                    count_int += 1
                    points.append(p)

            #planes fixed in y
            if (i == 2) or (i == 3):

                if (p[0] > xlim[0] and p[0] < xlim[1]) and (p[2] > zlim[0] and p[2] < zlim[1]):
                    
                    count_int += 1
                    points.append(p)

            #planes fixed in z
            if (i == 4) or (i == 5):

                if (p[0] > xlim[0] and p[0] < xlim[1]) and (p[1] > ylim[0] and p[1] < ylim[1]):

                    count_int += 1
                    points.append(p)
        
        #Require at least two intersections
        if count_int == 2:

            count_tot += 1

    #return percentage of intersections along with intersection points
    return [count_tot/len(extrinsics), np.array(points)]

if __name__ == '__main__':
    transforms_data = json.load(open('./data/outputs/Local_Test/transforms_data.json'))
    extrinsics = np.array([np.array(frame['extrinsic_matrix']) for frame in transforms_data['frames']])
    intrinsic = transforms_data['intrinsic_matrix']
    
    xlim = [-1, 1]
    ylim = [-1, 1]
    zlim = [-1, 1]

    lims = np.array([xlim, ylim, zlim])

    out = counter(extrinsics, intrinsic, lims)
    print(out[0])

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

        l = matrix @ np.array([0, 0, -1, 1], )
        l = l[:3]
        l_0 = matrix[:, 3][:3]

        #uncomment this to plot direction vectors
        ax.plot([l_0[0], l[0]], [l_0[1], l[1]], [l_0[2], l[2]], color = 'black', alpha = 0.5)

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

    ax.scatter(0, 0, 0, color = 'black', marker = '+', )
    ax.scatter(C[0], C[1], C[2], c = np.arange(len(C[0])))

    for point in out[1]:
        ax.scatter(point[0], point[1], point[2], color = 'black', marker = ',')



    plt.show()
