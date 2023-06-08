# -*- coding : utf-8-*-

import ast
import os
import serial
import time
import threading
import imageUpload as up
import RPi.GPIO as GPIO
from datetime import datetime


connect_status = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
PWM_output_left = GPIO.PWM(12, 600)
PWM_output_right = GPIO.PWM(13, 600)


class Asparagus_car:
    def __init__(self):
        # Define the pin number
        self.Pin1 = 6
        self.Pin2 = 5
        self.Pin3 = 19
        self.Pin4 = 16
        self.PWMPin_left  = 12
        self.PWMPin_right = 13

        # Initial the status
        self.speed = 0
        self.status  = "s"  # Forward, Stop, Backword

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.Pin1, GPIO.OUT)
        GPIO.setup(self.Pin2, GPIO.OUT)
        GPIO.setup(self.Pin3, GPIO.OUT)
        GPIO.setup(self.Pin4, GPIO.OUT)
        GPIO.setup(self.PWMPin_left, GPIO.OUT)
        GPIO.setup(self.PWMPin_right, GPIO.OUT)
        GPIO.output(self.Pin1, GPIO.LOW)
        GPIO.output(self.Pin2, GPIO.LOW)
        GPIO.output(self.Pin3, GPIO.LOW)
        GPIO.output(self.Pin4, GPIO.LOW)
        PWM_output_left.start(self.speed)
        PWM_output_right.start(self.speed)
        print("Car ready")

    def __capture(self, location='error_p'):
        now = datetime.now().strftime('%Y%m%d_%H_%M_%S')
        path = "/home/pi/Desktop/photo_record/left/"
        if not os.path.isdir(path):
            os.makedirs(path, mode=0o777)

        filename = f"{now}-{location}.jpg"
        action_left = f'libcamera-still -n -t 1 -o {path}/{filename} --width 1920 --height 1080'  # 1920x1080
        # action_left = f'libcamera-still -n -t 1 -o {folder}/{filename}'  # 3280x2464
        os.system(action_left)

        up.side(section=location, imagepath=f'{path}/{filename}')
        time.sleep(1.2)
        print('saved')

    def __slow_down(self):
        if self.status == "b" or self.status == "f":
            while self.speed > 0:
                self.speed = self.speed - 3
                if self.speed < 0:
                    break
                PWM_output_left.ChangeDutyCycle(self.speed)
                PWM_output_right.ChangeDutyCycle(self.speed)
                time.sleep(0.1)
        self.speed = 0
        PWM_output_left.ChangeDutyCycle(self.speed)
        PWM_output_right.ChangeDutyCycle(self.speed)

    def __change_direct(self, direction="s", section_r='error_p', section_l='error_p'):
        # self.__slow_down()
        self.status = direction
        if direction == "s":
            self.__slow_down()
            GPIO.output(self.Pin1, GPIO.LOW)
            GPIO.output(self.Pin2, GPIO.LOW)
            GPIO.output(self.Pin3, GPIO.LOW)
            GPIO.output(self.Pin4, GPIO.LOW)

        elif direction == "f":
            # self.__slow_down()
            GPIO.output(self.Pin1, GPIO.HIGH)
            GPIO.output(self.Pin2, GPIO.LOW)
            GPIO.output(self.Pin3, GPIO.HIGH)
            GPIO.output(self.Pin4, GPIO.LOW)

        elif direction == "b":
            self.__slow_down()
            GPIO.output(self.Pin1, GPIO.LOW)
            GPIO.output(self.Pin2, GPIO.HIGH)
            GPIO.output(self.Pin3, GPIO.LOW)
            GPIO.output(self.Pin4, GPIO.HIGH)

        elif direction == "r":
            GPIO.output(self.Pin1, GPIO.HIGH)
            GPIO.output(self.Pin2, GPIO.LOW)
            GPIO.output(self.Pin3, GPIO.HIGH)
            GPIO.output(self.Pin4, GPIO.LOW)

        elif direction == "l":
            GPIO.output(self.Pin1, GPIO.HIGH)
            GPIO.output(self.Pin2, GPIO.LOW)
            GPIO.output(self.Pin3, GPIO.HIGH)
            GPIO.output(self.Pin4, GPIO.LOW)

        elif direction == "p":
            GPIO.output(self.Pin1, GPIO.LOW)
            GPIO.output(self.Pin2, GPIO.LOW)
            GPIO.output(self.Pin3, GPIO.LOW)
            GPIO.output(self.Pin4, GPIO.LOW)
            self.__capture(location=section_l)
            self.status = "s"

    def __speed_up(self, direction, top_speed, speed_l, speed_r):
        if direction == "l" or direction == "r":
            try:
                PWM_output_left.ChangeDutyCycle(speed_l)
                PWM_output_right.ChangeDutyCycle(speed_r)
            except:
                pass
        else:
            if self.speed <= top_speed:
                self.speed = self.speed + 2
                PWM_output_left.ChangeDutyCycle(self.speed)
                PWM_output_right.ChangeDutyCycle(self.speed)


    def drive(self, direction="s", top_speed=10, speed_l=5, speed_r=5, section_r='E36', section_l='error_p'):
        if direction != self.status:
            self.__change_direct(direction, section_r, section_l)
        else:
            if direction != "s":
                self.__speed_up(direction, top_speed, speed_l, speed_r)

    def parking(self):
        self.__slow_down()
        self.status = "s"
        GPIO.output(self.Pin1, GPIO.LOW)
        GPIO.output(self.Pin2, GPIO.LOW)
        GPIO.output(self.Pin3, GPIO.LOW)
        GPIO.output(self.Pin4, GPIO.LOW)
        PWM_output_left.stop()
        PWM_output_right.stop()
        GPIO.cleanup()

def receive_motot_pwm():
    ser = serial.Serial(port='/dev/ttyS0', baudrate=115200, timeout=0.1)
    try:
        singnal = ser.readline()
        ser.flush()
    finally:
        ser.close()
    ser.close()
    return singnal


# 原本是send_motor_pwm，被搞死..
def send_message_to_rpi_right(direction, section_r):
    pwm = {'direction': direction, 'section_r': section_r}
    ser = serial.Serial(port='/dev/ttyAMA1', baudrate=115200, timeout=0.3,)
    ser.write(bytes(str(pwm), 'utf-8'))
    ser.flush()
    time.sleep(0.1)
    print(pwm)
    ser.close()


def job():
    global data, speed_left, speed_right, speed_top, section_r, section_l
    while connect_status == 1:
        singnal = receive_motot_pwm().decode(errors='ignore')
        try:
            singnal_dict = ast.literal_eval(singnal)
            print(singnal_dict)
            data_messsage = singnal_dict['direction']
            speed_left = round(singnal_dict['left'], 2)
            speed_right = round(singnal_dict['right'], 2)
            speed_top = (speed_left + speed_right) / 2
            section_r = singnal_dict['section_r']
            section_l = singnal_dict['section_l']
            send_message_to_rpi_right(data_messsage, str(section_r))

            if 'left' in singnal_dict['direction']:
                data = "l"
            elif 'right' in singnal_dict['direction']:
                data = "r"
            elif 'photo' in singnal_dict['direction']:
                data = "p"
            elif 'mid' in singnal_dict['direction']:
                data = "f"
            else:
                data = "s"
        except:
            pass
    GPIO.cleanup()


count = 0
time.sleep(5)
mycar = Asparagus_car()
data = "s"
speed_left = 0
speed_right = 0
speed_top = 0
section_r = 'error_p'
section_l = 'error_p'
connect_status = 1
try:
    t = threading.Thread(target=job)
    t.start()
    while True:
        pr_data = data
        mycar.drive(
            pr_data,
            top_speed=speed_top,
            speed_l=speed_left,
            speed_r=speed_right,
            section_r=section_r,
            section_l=section_l,
        )
        # send_motor_pwm(pr_data,speed_right,speed_left,str(section_r))
        time.sleep(0.1)
        count += count

finally:
    mycar.parking()
    GPIO.cleanup()
