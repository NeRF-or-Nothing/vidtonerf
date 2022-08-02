FROM nvidia/cuda:10.2-devel-ubuntu18.04

ENV colmap_v=3.7
ENV cmake_v=3.21.0
ENV opencv_v=4.5.5.62
ENV ceres_solver_v=2.0.0

RUN echo "apt packages" \
	&& export DEBIAN_FRONTEND=noninteractive \
	&& apt -y update --no-install-recommends \
	&& apt -y install --no-install-recommends \
	git \
	wget \
	ffmpeg \
	tk-dev \
	libxi-dev \
	libc6-dev \
	libbz2-dev \
	libffi-dev \
	libomp-dev \
	libssl-dev \
	zlib1g-dev \
	libcgal-dev \
	libgdbm-dev \
	libglew-dev \
	python3-dev \
	python3-pip \
	qtbase5-dev \
	checkinstall \
	libglfw3-dev \
	libeigen3-dev \
	libgflags-dev \
	libxrandr-dev \
	libopenexr-dev \
	libsqlite3-dev \
	libxcursor-dev \
	build-essential \
	libcgal-qt5-dev \
	libxinerama-dev \
	libboost-all-dev \
	libfreeimage-dev \
	libncursesw5-dev \
	libatlas-base-dev \
	libqt5opengl5-dev \
	libgoogle-glog-dev \
	libsuitesparse-dev \
	python3-setuptools \
	libreadline-gplv2-dev \
	&& apt autoremove -y \
	&& apt clean -y \
	&& export DEBIAN_FRONTEND=dialog

RUN echo "pip packages" \
	&& python3 -m pip install -U pip && pip3 --no-cache-dir install cmake==${cmake_v} opencv-python==${opencv_v} 

RUN echo "Ceres Solver" \
	&& cd /opt && git clone https://github.com/ceres-solver/ceres-solver \
	&& cd ./ceres-solver && git checkout ${ceres_solver_v} \
	&& mkdir ./build && cd ./build && cmake ../ -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF \
	&& make -j && make install

RUN echo "COLMAP" \
	&& cd /opt && git clone https://github.com/colmap/colmap \
	&& cd ./colmap && git checkout ${colmap_v} \
	&& mkdir ./build && cd ./build && cmake ../ \
	&& make -j && make install && colmap -h