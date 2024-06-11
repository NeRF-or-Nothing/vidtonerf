
# Original environment.yml:
name: gaussian_splatting
channels:
  - pytorch
  - conda-forge
  - defaults
dependencies:
  - cudatoolkit=11.6
  - plyfile
  - python=3.7.13
  - pip=22.3.1
  - pytorch=1.12.1
  - torchaudio=0.12.1
  - torchvision=0.13.1
  - tqdm
  - pip:
    - submodules/diff-gaussian-rasterization
    - submodules/simple-knn


# Train.py
Reduced:
 Insert HERE

## Imports:
os, torch, randint, utils.loss_utils, gaussian_renderer, sys,
scene, utils.general_utils, uuid, tqdm, argparse, arguments, 

Get rid of network_gui, and will try to build to smaller image by removing extras once
gaussian rasterizer and simple knn cuda compiled

# Render.py
Reduced: 
 Insert HERE

## Imports:
os, torhc, scene.Scene, tqdm, gaussian_renderer, torchvision,
utils.general_utils, argprase, arguments, gaussian_renderer


# Needed:
gaussian_renderer: Renders the actual scene
arguments: inputs for `train.py`, `render.py`
utils: utility functions for `train.py`, `render.py` 
scene: 

# Not Needed:
SIBR_viewers

