#FROM nvidia/cuda:10.2-devel-ubuntu18.04
FROM colmap/colmap:latest

# https://forums.developer.nvidia.com/t/gpg-error-http-developer-download-nvidia-com-compute-cuda-repos-ubuntu1804-x86-64/212904
# Updating GPG Key for Nvidia manually
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/3bf863cc.pub
RUN export DEBIAN_FRONTEND=noninteractive && \
	apt-get update -y  && \
	apt-get install libssl-dev -y && \
	apt-get install software-properties-common -y && \
	add-apt-repository ppa:deadsnakes/ppa && \
	apt-get update -y  && \
	apt-get install curl -y && \
	apt-get install python3.10 -y && \
	apt-get install python3-pip -y 


WORKDIR /sfmworker
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
# Requirements.txt copied seperately to utilize docker build cache
COPY ./requirements.txt /sfmworker
RUN python3.10 -m pip install --upgrade -r requirements.txt

COPY . /sfmworker/

#CMD ["python3", "-V"]
CMD ["python3.10", "main.py", "--config=configs/default.txt"]