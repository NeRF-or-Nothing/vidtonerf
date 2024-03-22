import unittest
import numpy as np
from matrix import euler_from_quaternion, quaternion_rotation_matrix, rotation_matrix_from_vectors

class TestMatrixFunctions(unittest.TestCase):

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

    
if __name__ == '__main__':
    unittest.main()