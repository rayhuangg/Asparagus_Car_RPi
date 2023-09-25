# -*- coding : utf-8-*-

import os
import socket
import serial
import threading
import time
from datetime import datetime
import RPi.GPIO as GPIO
from getkey import getkey, keys
import imageUpload as up
from asparagus_car import AsparagusCar


if __name__ == "__main__":
    mycar = AsparagusCar()
    try:
        while True:
            print("Waiting to press... Press p to take photo and upload.")
            key = getkey()
            hostname = socket.gethostname()
            if key == 'p':
                print("Receive key 'p'")
                if hostname == "raspberrypi-1dinci":
                    # capture(location="B1")
                    mycar.capture()
                elif hostname == "raspberrypi-2dinci":
                    # capture(location="A1")
                    mycar.capture()

    except KeyboardInterrupt:
        print("bye.")