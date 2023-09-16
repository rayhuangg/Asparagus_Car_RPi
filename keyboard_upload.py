# -*- coding : utf-8-*-

import os
import socket
import serial
import threading
import time
from datetime import datetime

import imageUpload as up
import RPi.GPIO as GPIO
from getkey import getkey, keys


def capture(location='unspecified'):
    hostname = socket.gethostname()
    now = datetime.now().strftime('%Y%m%d_%H_%M_%S')
    if hostname == "raspberrypi-1dinci":
        path = "/home/pi/Desktop/photo_record/left/"
    elif hostname == "raspberrypi-2dinci":
        path = "/home/pi/Desktop/photo_record/right/"

    if not os.path.isdir(path):
        os.makedirs(path, mode=0o777)

    filename = f"{now}-{location}.jpg"
    # action = f'libcamera-still -n -t 1 -o {path}/{filename}'  # 3280x2464
    action = f'libcamera-still -n -t 1 -o {path}/{filename} --width 1920 --height 1080'  # 1920x1080
    os.system(action)

    up.side(section=location, imagepath=f'{path}/{filename}')
    time.sleep(1.2)
    print('photo saved and upload successed')


if __name__ == "__main__":
    try:
        while True:
            print("Waiting to press... Press p to take photo and upload.")
            key = getkey()
            hostname = socket.gethostname()
            if key == 'p':
                print("Receive key 'p'")
                if hostname == "raspberrypi-1dinci":
                    capture(location="B1")
                elif hostname == "raspberrypi-2dinci":
                    capture(location="A1")

    except KeyboardInterrupt:
        print("bye.")