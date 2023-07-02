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

connect_status = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
PWMfun = GPIO.PWM(12, 600)
PWMfun2 = GPIO.PWM(13, 600)


def send_message_to_rpi_right(direction, section_r="dont take"):
    pwm = {'direction': direction, 'section_r': section_r}
    ser = serial.Serial(
        port='/dev/ttyAMA1',  # Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate=115200,
        timeout=0.3,
    )

    ser.write(bytes(str(pwm), 'utf-8'))
    ser.flush()
    time.sleep(0.1)
    print(pwm)
    ser.close()


def capture(location='A3'):
    now = datetime.now().strftime('%Y%m%d_%H_%M_%S')

    folder = "/home/pi/Desktop/photo_record/left/"
    if not os.path.isdir(folder):
        os.makedirs(mode=0o777)

    filename = f"{now}-{location}.jpg"
    action_left = f'libcamera-still -n -t 1 -o {folder}/{filename}' # Full resulation
    # action_left = f'libcamera-still -n -t 1 -o {folder}/{filename} --width 1920 --height 1080'

    os.system(action_left)
    # print(location)
    # up.side(section=location , imagepath=f'{folder}/{filename}')
    # time.sleep(1.2)
    print('saved')


if __name__ == "__main__":
    while True:
        print("Waiting to press... Press p to take photo and upload.")
        key = getkey()
        # 获取计算机的主机名
        hostname = socket.gethostname()
        if key == 'p':
            print("Receive key 'p'")
            capture(location="B1")
