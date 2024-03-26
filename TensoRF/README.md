# TensoRF
### This code is based on a research project located [here](https://apchenstu.github.io/TensoRF/) with the readme included below.
A single threaded worker that runs this project consuming jobs from RabbitMQ and submitting it back to a seperate completed job queue is located at `worker.py`. This worker loads the config file at `configs/workerconfig.txt` that defines the settings TensoRF should be run at to process each job. Right now the config is static but in the future these settings can be modified based on the job.

The worker consumes jobs from RabbitMQ described via a json template that contains the following:
```
{
	"id": String,
	"vid_width": int,
	"vid_height": int,
	"trained_model_file": String(optional),
	"intrinsic_matrix": float[[]],
	 "frames": [
		 {
		   "file_path": String
		   "extrinsic_matrix": float[[]]
		 }, 
		...
		  ]
 }
 ```

Once the worker is done generating the trained NeRF and rendering the desired video it submits a complete forum to RabbitMQ also in the json format that contains the following:
```
{
	"id": String,
	"model_file": String,
	"video_file": String
}
```

# Usage of Local Worker
Here are some basic instructions on how to use the worker.py in local mode:
### Running worker.py
To run worker.py to train a new TensoRF and render a new video use the command: `python worker.py --config configs/localworkerconfig.txt`. 

If you only want to render a new video from a TensoRF model that has already been trained use the command:
`python worker.py --config configs/localworkerconfig.txt --ckpt [PATH TO TENSORF MODEL] --render_only 1` 
This will load a model from the specified path and use it to render the camera motion specified in the `transforms_render.json` input file.

Example for render only: `python worker.py --config configs/localworkerconfig.txt --ckpt log/tensorf_sfm_data_VM/tensorf_sfm_data_VM.th --render_only 1`
### Input data
The worker takes input from `data/sfm_data/`. Within this folder you should provide a json file named `transforms_train.json` which will contain the transformation data from structure from motion along with a subfolder labeled `train` that will contain all of the image files referenced in `transforms_train.json`. This will provide the worker with all the data it needs to train a TensoRF. Then once the TensoRF model is trained the worker will load the final file from the input data `transforms_render.json` which contains the desired camera path to be rendered in the same format as the training json (template above)

Example input file structure:

![Screenshot_20220729_065836](https://user-images.githubusercontent.com/49171429/181745902-920d5483-28e6-4412-bc07-9c770544057f.png)

### Output data
The worker outputs final results to `log/tensorf_sfm_data_VM`.

Within this folder the only relevate outputs for the worker are the rendered images and final video in the `imgs_render_all` folder and the trained TensoRF model that is saved at `tensorf_sfm_data.th`. This trained model can be reused by the worker using the checkpoint `--ckpt` flag.


## [Project page](https://apchenstu.github.io/TensoRF/) |  [Paper](https://arxiv.org/abs/2203.09517)
This repository contains a pytorch implementation for the paper: [TensoRF: Tensorial Radiance Fields](https://arxiv.org/abs/2203.09517). Our work present a novel approach to model and reconstruct radiance fields, which achieves super
**fast** training process, **compact** memory footprint and **state-of-the-art** rendering quality.<br><br>


https://user-images.githubusercontent.com/16453770/158920837-3fafaa17-6ed9-4414-a0b1-a80dc9e10301.mp4
## Installation

#### Tested on Ubuntu 20.04 + Pytorch 1.10.1 

Install environment:
```
conda create -n TensoRF python=3.8
conda activate TensoRF
pip install torch torchvision
pip install tqdm scikit-image opencv-python configargparse lpips imageio-ffmpeg kornia lpips tensorboard
pip install -r requirements.txt
```


## Dataset
* [Synthetic-NeRF](https://drive.google.com/drive/folders/128yBriW1IG_3NJ5Rp7APSTZsJqdJdfc1) 
* [Synthetic-NSVF](https://dl.fbaipublicfiles.com/nsvf/dataset/Synthetic_NSVF.zip)
* [Tanks&Temples](https://dl.fbaipublicfiles.com/nsvf/dataset/TanksAndTemple.zip)
* [Forward-facing](https://drive.google.com/drive/folders/128yBriW1IG_3NJ5Rp7APSTZsJqdJdfc1)



## Quick Start
The training script is in `train.py`, to train a TensoRF:

```
python train.py --config configs/lego.txt
```


we provide a few examples in the configuration folder, please note:

 `dataset_name`, choices = ['blender', 'llff', 'nsvf', 'tankstemple'];

 `shadingMode`, choices = ['MLP_Fea', 'SH'];

 `model_name`, choices = ['TensorVMSplit', 'TensorCP'], corresponding to the VM and CP decomposition. 
 You need to uncomment the last a few rows of the configuration file if you want to training with the TensorCP model；

 `n_lamb_sigma` and `n_lamb_sh` are string type refer to the basis number of density and appearance along XYZ
dimension;

 `N_voxel_init` and `N_voxel_final` control the resolution of matrix and vector;

 `N_vis` and `vis_every` control the visualization during training;

  You need to set `--render_test 1`/`--render_path 1` if you want to render testing views or path after training. 

More options refer to the `opt.py`. 

### For pretrained checkpoints and results please see:
[https://1drv.ms/u/s!Ard0t_p4QWIMgQ2qSEAs7MUk8hVw?e=dc6hBm](https://1drv.ms/u/s!Ard0t_p4QWIMgQ2qSEAs7MUk8hVw?e=dc6hBm)



## Rendering

```
python train.py --config configs/lego.txt --ckpt path/to/your/checkpoint --render_only 1 --render_test 1 
```

You can just simply pass `--render_only 1` and `--ckpt path/to/your/checkpoint` to render images from a pre-trained
checkpoint. You may also need to specify what you want to render, like `--render_test 1`, `--render_train 1` or `--render_path 1`.
The rendering results are located in your checkpoint folder. 

## Extracting mesh
You can also export the mesh by passing `--export_mesh 1`:
```
python train.py --config configs/lego.txt --ckpt path/to/your/checkpoint --export_mesh 1
```
Note: Please re-train the model and don't use the pretrained checkpoints provided by us for mesh extraction, 
because some render parameters has changed.

## Training with your own data
We provide two options for training on your own image set:

1. Following the instructions in the [NSVF repo](https://github.com/facebookresearch/NSVF#prepare-your-own-dataset), then set the dataset_name to 'tankstemple'.
2. Calibrating images with the script from [NGP](https://github.com/NVlabs/instant-ngp/blob/master/docs/nerf_dataset_tips.md):
`python dataLoader/colmap2nerf.py --colmap_matcher exhaustive --run_colmap`, then adjust the datadir in `configs/your_own_data.txt`. Please check the `scene_bbox` and `near_far` if you get abnormal results.
    

## Citation
If you find our code or paper helps, please consider citing:
```
@INPROCEEDINGS{Chen2022ECCV,
  author = {Anpei Chen and Zexiang Xu and Andreas Geiger and Jingyi Yu and Hao Su},
  title = {TensoRF: Tensorial Radiance Fields},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year = {2022}
}
```
