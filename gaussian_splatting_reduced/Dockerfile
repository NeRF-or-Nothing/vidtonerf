FROM nvidia/cuda:11.7.1-devel-ubuntu20.04

# Set the environment variable to prevent apt from prompting for user input
ENV DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    libc6 \  
    && rm -rf /var/lib/apt/lists/*
# software-properties-common is needed for add-apt-repository
# libc6 updates glibc to 2.31 (newest compatible version with 20.04)

# Copy source code
COPY requirements.txt .
COPY . /gaussian_splatting_reduced
WORKDIR /gaussian_splatting_reduced

# Install dependencies (must get older python from non-default repo)
RUN add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    python3.8 \
    python3-pip \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.8 as the default Python version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Install Python dependencies (including prebuilt wheels)
RUN pip install -r requirements.txt

# Allow entry_point.sh to be executable
RUN ["chmod", "+x", "./entry_point.sh"]
RUN ["chmod", "+x", "./entry_point2.sh"]