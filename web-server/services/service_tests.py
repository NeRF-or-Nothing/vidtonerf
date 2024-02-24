import unittest
from queue_service import k_mean_sampling
import os
import json

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
            self.assertTrue(len(output_data) == 100)
            print(f"Loop {idx}:", output_data, '\n')

            new_frames = [input_data["frames"][x] for x in output_data]
            print(f"Loop {idx}:", new_frames, '\n')
            self.assertTrue(len(new_frames) == 100)


if __name__=='__main__':
    unittest.main()
