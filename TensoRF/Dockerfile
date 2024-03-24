
FROM python:3.10.8-slim

WORKDIR /TensoRF

# Change for deployment to local directory
COPY ./TensoRF/requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Overwritten by compose
COPY . .

CMD ["python3", "main.py"]
  