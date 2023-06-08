# -*- coding : utf-8-*-

import time
import RPi.GPIO as GPIO
import os
import io
from datetime import datetime
import serial
import ast
import threading
import imageUpload as up
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
    #     ser.write(str.encode(f'{counter}\n'))s
    ser.write(bytes(str(pwm), 'utf-8'))
    ser.flush()
    time.sleep(0.1)
    print(pwm)
    ser.close()


def capture(location='A3'):
    # send_message_to_rpi_right(direction="right", section_r="A3") # 測試 避免一直拍照
    now = datetime.now().strftime('%Y%m%d_%H_%M_%S')

    folder = "/home/pi/Desktop/photo_record/left/"
    if not os.path.isdir(folder):
        os.makedirs(mode=0o777)

    filename = f"{now}-{location}.jpg"
    # action_left = f'libcamera-still -n -t 1 -o {folder}/{filename} --width 1920 --height 1080'
    action_left = f'libcamera-still -n -t 1 -o {folder}/{filename}'

    # Old
    # action_right='libcamera-still -n -t 1 -o /home/pi/Desktop/photo_record/left/'+now + '.jpg --width 1920 --height 1080'
    # action_right='libcamera-still -n -t 1 -o /home/pi/Desktop/photo_record/right/'+now + '.jpg'

    os.system(action_left)
    # print(location)
    # up.side(section=location , imagepath=f'{folder}/{filename}')
    # time.sleep(1.2)
    print('saved')


if __name__ == "__main__":
    while True:
        print("Waiting to press... Press p to take photo and upload.")
        key = getkey()
        # print(key)
        if key == key == 'p':
            print("Receive key 'p'")
            capture(location="B1")
            # send_message_to_rpi_right(direction="photo", section_r="B1")
