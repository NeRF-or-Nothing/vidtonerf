#!/bin/bash

# This script is the entry point for the nerf-worker container.
# It installs the submodules that need nvcc to build, builds them, 
# and then runs the main Python script you would normally find in 
# the other service containers like sfm-worker.


# Change to the simple-knn directory
cd /submodules/simple-knn

# Build and install the wheel
python setup.py bdist_wheel
pip install dist/*

# Change to the diff-gaussian-rasterize directory
cd /submodules/diff-gaussian-rasterize

# Build and install the wheel
python setup.py bdist_wheel  
pip install dist/*

# Return to the base directory
cd /

# Run the main Python script
python main.py