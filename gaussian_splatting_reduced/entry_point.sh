#!/bin/bash

# This script is the entry point for the nerf-worker-gaussian container.
# It installs the submodules that need nvcc to build, builds them, 
# and then runs the main.py Python script you would normally find in 
# the other service containers like sfm-worker.

echo "Starting entry_point.sh"

# Change to the simple-knn directory
cd submodules/simple-knn
pwd
echo "Building simple-knn"
# Build and install the wheel
python setup.py bdist_wheel
pip install dist/*
echo "Finished building simple-knn"

# Change to the diff-gaussian-rasterize directory
cd ../diff-gaussian-rasterization
pwd
echo "Building diff-gaussian-rasterization"
# Build and install the wheel
python setup.py bdist_wheel  
pip install dist/*
echo "Finished building diff-gaussian-rasterization"

# Return to the base directory
cd ..
cd ..

# Run the main Python script
# python main.py
pwd
ls -la

python train.py -s data/sfm_data/TestUUID/ -m data/nerf_data/TestUUID