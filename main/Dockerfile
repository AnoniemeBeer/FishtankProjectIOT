FROM python:latest

COPY ./start.sh ./start.sh
COPY ./app.py ./app.py
COPY ./homebridge.py ./homebridge.py
COPY ./modules ./modules
COPY ./images/fish.png ./images/fish.png

RUN apt-get update

RUN apt-get install python3-pil
RUN apt-get install python3-pip
RUN pip3 install adafruit-circuitpython-pcd8544
RUN pip3 install requests

CMD ["bash", "start.sh"]