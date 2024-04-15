# Description: This script empties all the local run data, this
# is particularly useful when you want to keep the filesize small
# while debugging or testing the code.

find ./colmap/data/inputs -type f -delete
find ./colmap/data/outputs -mindepth 1 -delete
find ./TensoRF/data/sfm_data -mindepth 1 -delete
find ./TensoRF/data/nerf_data -mindepth 1 -delete
find ./TensoRF/log -mindepth 1 -delete
find ./web-server/data/nerf -mindepth 1 -delete
find ./web-server/data/raw/videos -mindepth 1 -delete
find ./web-server/data/sfm -mindepth 1 -delete