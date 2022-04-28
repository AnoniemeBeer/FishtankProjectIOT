#!/bin/bash

. streamSettings.config

ffmpeg -f v4l2 -s ${heigth}x${width} -input_format mjpeg -r ${webcamFramerate} -i /dev/video0 -vcodec libx264 -pix_fmt yuv420p -preset ultrafast -r ${streamFramerate} -g 20 -b:v 2500k -codec:a libmp3lame -ar 44100 -threads 6 -b:a 11025 -bufsize 512k -f flv ${streamUrl}/${streamKey}