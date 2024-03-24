
FROM python:3.10.8-slim

WORKDIR /TensoRF

# Change for deployment to local directory
COPY ./TensoRF/requirements.txt requirements.txt
RUN apt-get update
# TODO: Find the actually required package for libGL.so.1 to be on image
RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Overwritten by compose
COPY . .

CMD ["python3", "main.py"]
  