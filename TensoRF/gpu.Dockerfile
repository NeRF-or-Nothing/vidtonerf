# NVIDIA CUDA Toolkit 10.2 for ubuntu
FROM nvidia:10.2-devel-ubuntu18.04

WORKDIR /TensoRF

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/3bf863cc.pub
RUN export DEBIAN_FORNTEND=noninteractive && \
    apt-get update -y && \
    apt-get install libssl-dev -y && \
    apt-get install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update -y && \
    apt-get install curl -y && \
    apt-get install python3.10 -y && \
    apt-get install python3-pip -y

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

COPY ./TensoRF/requirements.txt requirements.txt
RUN python3.10 -m pip install --upgrade -r requirements.txt

# Overwritten by compose
COPY . .

# TODO add config support
CMD ["python3.1-0", "main.py"]]