import unittest
import numpy as np
from matrix import euler_from_quaternion, quaternion_rotation_matrix, rotation_matrix_from_vectors
from colmap_runner import run_colmap
import os
from pymongo import MongoClient

class Testcolmap(unittest.TestCase):

    def test_euler_from_quaternion(self):
        # Test case 1
        roll, pitch, yaw = euler_from_quaternion(0, 0, 0.7072, 0.7072)
        self.assertAlmostEqual(roll, 0)
        self.assertAlmostEqual(pitch, 0.0)
        self.assertAlmostEqual(yaw, 1.5710599372799763)

        # Test case 2
        roll, pitch, yaw = euler_from_quaternion(0.5, 0.5, 0.5, 0.5)
        self.assertAlmostEqual(roll, 1.5707963267948966)
        self.assertAlmostEqual(pitch, 0.0)
        self.assertAlmostEqual(yaw, 1.5707963267948966)

    def test_quaternion_rotation_matrix(self):
        # Test case 1
        rotation_matrix = quaternion_rotation_matrix(0.5, 0.5, 0.5, 0.5)
        expected_matrix = np.array([[0.0, 0.0, 1.0],
                                    [1.0, 0.0, 0.0],
                                    [0.0, 1.0, 0.0]])
        np.testing.assert_array_almost_equal(rotation_matrix, expected_matrix)

        # Test case 2
        rotation_matrix = quaternion_rotation_matrix(0.0, 0.0, 0.0, 1.0)
        expected_matrix = np.array([[-1.0, 0.0, 0.0],
                                    [0.0, -1.0, 0.0],
                                    [0.0, 0.0, 1.0]])
        np.testing.assert_array_almost_equal(rotation_matrix, expected_matrix)

    def test_rotation_matrix_from_vectors(self):
        # Test case 1
        vec1 = np.array([1.0, 0.0, 0.0])
        vec2 = np.array([0.0, 1.0, 0.0])
        rotation_matrix = rotation_matrix_from_vectors(vec1, vec2)
        expected_matrix = np.array([[0.0, -1.0, 0.0],
                                    [1.0, 0.0, 0.0],
                                    [0.0, 0.0, 1.0]])
        np.testing.assert_array_almost_equal(rotation_matrix, expected_matrix)

        # Test case 2
        vec1 = np.array([1.0, 0.0, 0.0])
        vec2 = np.array([0.0, 0.0, 1.0])
        rotation_matrix = rotation_matrix_from_vectors(vec1, vec2)
        expected_matrix = np.array([[0.0, 0.0, -1.0],
                                    [0.0, 1.0, 0.0],
                                    [1.0, 0.0, 0.0]])
        np.testing.assert_array_almost_equal(rotation_matrix, expected_matrix)

    def test_colmap_runner(self):
        # Test case 1
        instance_name = "colmap_output"
        output_path = "."
        colmap_path = r".\colmap.exe"
        images_path = r".\data\inputs\transforms_bear"

        # Run COLMAP and ensure that there are no errors
        status = run_colmap(colmap_path, images_path, output_path)
        self.assertEqual(status, 0)

        # Test case 2
        instance_name = "colmap_output"
        output_path = "."
        colmap_path = r".\colmap.exe"
        images_path = r".\data\inputs\transforms_otter"

        status = run_colmap(colmap_path, images_path, output_path)
        self.assertEqual(status, 0)

if __name__ == '__main__':
    unittest.main()