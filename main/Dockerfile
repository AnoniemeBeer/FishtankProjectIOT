FROM python:latest

COPY ./start.sh ./start.sh
COPY ./app.py ./app.py
COPY ./homebridge.py ./homebridge.py
COPY ./modules ./modules
COPY ./images/fish.png ./images/fish.png

RUN apt-get update

 RUN pip install --no-cache-dir rpi.gpio &&\
    pip install adafruit-blinka &&\
    pip install adafruit-circuitpython-pcd8544 &&\
    pip install pillow &&\
    pip install requests &&\
    pip install ply &&\
    pip install jinja2 &&\
    pip install pyyaml

CMD ["bash", "start.sh"]
