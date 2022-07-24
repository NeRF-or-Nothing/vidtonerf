#Dockerized Ubuntu SSH service from https://registry.hub.docker.com/u/rastasheep
FROM       ubuntu:latest 

RUN apt-get update

RUN apt-get install -y openssh-server
RUN mkdir /var/run/sshd

RUN echo 'root:root' |chpasswd

RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config

RUN mkdir /root/.ssh

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 22

CMD    ["/usr/sbin/sshd", "-D"]



# commands run within the docker container to setup the conda environment for TensoRF paper, and installing cuda to use
# nvidia gpus


#FROM       ubuntu:latest 
#ENV PATH="/root/miniconda3/bin:${PATH}"
#ARG PATH="/root/miniconda3/bin:${PATH}"
#RUN apt-get update
#RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*
#RUN wget \
    #https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    #&& mkdir /root/.conda \
    #&& bash Miniconda3-latest-Linux-x86_64.sh -b \
    #&& rm -f Miniconda3-latest-Linux-x86_64.sh 
#RUN conda --version
#RUN conda create -n TensoRF python=3.8
#RUN pip install torch torchvision
#RUN pip install tqdm scikit-image opencv-python configargparse lpips imageio-ffmpeg kornia lpips tensorboard
#RUN apt-get install git
#RUN git clone https://github.com/apchenstu/TensoRF
#RUN apt-get update && apt-get install -y gnupg
#RUN apt-key del 7fa2af80
#RUN wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
#RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/3bf863cc.pub
#RUN apt-get update && apt-get install -y gnupg
#RUN apt-get install -y software-properties-common
#RUN add-apt-repository ppa:libreoffice/ppa
#RUN apt update
#RUN apt install -y libreoffice
#RUN mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
#RUN wget https://developer.download.nvidia.com/compute/cuda/11.7.0/local_installers/cuda-repo-wsl-ubuntu-11-7-local_11.7.0-1_amd64.deb
#RUN dpkg -i cuda-repo-wsl-ubuntu-11-7-local_11.7.0-1_amd64.deb
#RUN wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.0-1_all.deb
#RUN dpkg -i cuda-keyring_1.0-1_all.deb
#RUN dpkg -i cuda-repo-wsl-ubuntu-11-7-local_11.7.0-1_amd64.deb
#RUN apt-get update
#RUN apt-get -y install cuda