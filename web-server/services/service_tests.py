import unittest
from queue_service import k_mean_sampling, find_elbow_point
import os
import json
import matplotlib.pyplot as plt
import math
import numpy as np

# Note: Have to copy scene.py into this directory to run this file

class k_meanTest(unittest.TestCase):
    # This function reads in all the files from k_mean_test_data
    def setUp(self):
        self.files = []
        for root, dirs, files in os.walk("./k_mean_test_data"):
            for file in files:
                if file.endswith('.json'):
                    self.files.append(os.path.join(root, file))
    
    # Get data from a json file
    def read_json_file(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    # First test case
    def test_vid(self):
        for x, idx in enumerate(self.files):
            input_data = self.read_json_file(self.files[x])
            output_data = k_mean_sampling(input_data)
            print(f"Loop {idx}:", output_data, '\n')

            new_frames = [input_data["frames"][x] for x in output_data]
            print(f"Loop {idx}:", new_frames, '\n')
    

class elbow_test():
    # This function reads in all the files from k_mean_test_data
    def setUp(self):
        self.files = []
        for root, dirs, files in os.walk("./k_mean_test_data"):
            for file in files:
                if file.endswith('.json'):
                    self.files.append(os.path.join(root, file))
    
    # Get data from a json file
    def read_json_file(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def preprocess_data(self, idx):
        # Generate sample data
        data = self.read_json_file(self.files[idx])

        # Copied from k_mean
        extrins = []
        angles = []
        for f in data["frames"]:
            extrinsic = np.array(f["extrinsic_matrix"])
            extrins+=[ extrinsic ]
        for i,e in enumerate(extrins):

            # t == rectangular coordinates
            t = e[0:3,3]

            # s == spherical coordinates

            # r = sqrt(x^2 + y^2 + z^2)
            r = math.sqrt((t[0]*t[0])+(t[1]*t[1])+(t[2]*t[2]))
            theta = math.acos(t[2]/r)
            phi = math.atan(t[1]/t[0])

            #convert radian to degrees

            theta = (theta * 180) / math.pi
            phi = (phi * 180) / math.pi

            s = [theta,phi]

            angles.append(s)
        return angles

    # Plotting the Elbow Method graph
    def plot_elbow_method(self, x, wcss):
        plt.plot(x, wcss)
        plt.title('Elbow Method')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
        plt.show()

    def test_elbow_point(self):
        self.setUp()
        for idx, _ in enumerate(self.files):
            angles = self.preprocess_data(idx)
            elbow_point, x, wcss = find_elbow_point(angles)
            print("Elbow point found at k =", elbow_point)

            self.plot_elbow_method(x, wcss)



if __name__=='__main__':
    elbow_test_instance = elbow_test()
    elbow_test_instance.test_elbow_point()

