FROM python:3.10.8-slim

WORKDIR /web-server

COPY ./web-server/requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Overwritten by compose
COPY . .

CMD ["python3", "main.py"]
