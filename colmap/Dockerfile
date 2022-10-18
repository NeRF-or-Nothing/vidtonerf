#FROM nvidia/cuda:10.2-devel-ubuntu18.04
FROM colmap/colmap:latest

# https://forums.developer.nvidia.com/t/gpg-error-http-developer-download-nvidia-com-compute-cuda-repos-ubuntu1804-x86-64/212904
# Updating GPG Key for Nvidia manually
RUN apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/3bf863cc.pub
RUN apt-get update -y  && \
	apt-get install python3-pip -y

WORKDIR /sfmworker
COPY . /sfmworker/
RUN pip3 install --upgrade pip && \
	pip3 install -r requirements.txt

CMD ["python3", "main.py"]