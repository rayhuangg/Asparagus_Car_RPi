#-*- coding : utf-8-*-

import time
import RPi.GPIO as GPIO
import os
import io
from datetime import datetime
import serial
import ast
import threading
import imageUpload as up
# from pynput import keyboard


connect_status = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
PWMfun=GPIO.PWM(12,600)
PWMfun2=GPIO.PWM(13,600)

class Asparagus_car:
    def __init__(self):
        self.Pin1=6
        self.Pin2=5
        self.PWMPin=12
        self.Pin3=19
        self.Pin4=16
        self.PWMPin2=13
        self.status="s"#Forward,Stop,Backword
        self.speed=0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.Pin1,GPIO.OUT)
        GPIO.setup(self.Pin2,GPIO.OUT)
        GPIO.setup(self.Pin3,GPIO.OUT)
        GPIO.setup(self.Pin4,GPIO.OUT)
        GPIO.setup(self.PWMPin,GPIO.OUT)
        GPIO.setup(self.PWMPin2,GPIO.OUT)
        GPIO.output(self.Pin1,GPIO.LOW)
        GPIO.output(self.Pin2,GPIO.LOW)
        GPIO.output(self.Pin3,GPIO.LOW)
        GPIO.output(self.Pin4,GPIO.LOW)
        #PWMfun=GPIO.PWM(self.PWMPin,600)
        #PWMfun2=GPIO.PWM(self.PWMPin2,600)
        PWMfun.start(self.speed)
        PWMfun2.start(self.speed)
        print("Car ready")

    def __capture(self,location='error_p'):
        print("enter capture")
        now = datetime.now().strftime('%Y%m%d_%H_%M_%S')

        folder = "/home/pi/Desktop/photo_record/right/"
        if not os.path.isdir(folder):
            os.makedirs(mode=0o777)

        filename = f"{now}-{location}.jpg"
        # action_right = f'libcamera-still -n -t 1 -o {folder}/{filename} --width 1920 --height 1080'
        action_right = f'libcamera-still -n -t 1 -o {folder}/{filename}'

        # Old
        # action_right='libcamera-still -n -t 1 -o /home/pi/Desktop/photo_record/right/'+now + '.jpg --width 1920 --height 1080'
        # action_right='libcamera-still -n -t 1 -o /home/pi/Desktop/photo_record/right/'+now + '.jpg'

        os.system(action_right)
        #print(location)
        up.side(section = location, imagepath = f'{folder}/{filename}')
        time.sleep(1.2)
        print('saved')

    def __slow_down(self):
        if self.status=="b" or self.status=="f" :
            while(self.speed>0):
                self.speed=self.speed-3
                if self.speed< 0:
                    break
                PWMfun.ChangeDutyCycle(self.speed)
                PWMfun2.ChangeDutyCycle(self.speed)
                time.sleep(0.1)
        self.speed=0
        PWMfun.ChangeDutyCycle(self.speed)
        PWMfun2.ChangeDutyCycle(self.speed)
    def __change_direct(self,direction="s",section_r='error_p'):
        # self.__slow_down()
        print("__change dir", direction, section_r)
        self.status=direction
        if direction=="s":
            self.__slow_down()
            #GPIO.output(self.PWMPin,GPIO.LOW)
            #GPIO.output(self.PWMPin2,GPIO.LOW)
            GPIO.output(self.Pin1,GPIO.LOW)
            GPIO.output(self.Pin2,GPIO.LOW)
            GPIO.output(self.Pin3,GPIO.LOW)
            GPIO.output(self.Pin4,GPIO.LOW)
        elif direction=="f":
            # self.__slow_down()
            #GPIO.output(self.PWMPin,GPIO.LOW)
            #GPIO.output(self.PWMPin2,GPIO.LOW)
            GPIO.output(self.Pin1,GPIO.HIGH)
            GPIO.output(self.Pin2,GPIO.LOW)
            GPIO.output(self.Pin3,GPIO.HIGH)
            GPIO.output(self.Pin4,GPIO.LOW)
        elif direction=="b":
            self.__slow_down()
            #GPIO.output(self.PWMPin,GPIO.LOW)
            #GPIO.output(self.PWMPin2,GPIO.LOW)
            GPIO.output(self.Pin1,GPIO.LOW)
            GPIO.output(self.Pin2,GPIO.HIGH)
            GPIO.output(self.Pin3,GPIO.LOW)
            GPIO.output(self.Pin4,GPIO.HIGH)
        elif direction=="r":
            #GPIO.output(self.PWMPin,GPIO.LOW)
            #GPIO.output(self.PWMPin2,GPIO.LOW)
            GPIO.output(self.Pin1,GPIO.HIGH)
            GPIO.output(self.Pin2,GPIO.LOW)
            GPIO.output(self.Pin3,GPIO.HIGH)
            GPIO.output(self.Pin4,GPIO.LOW)

        elif direction=="l":
            #GPIO.output(self.PWMPin,GPIO.LOW)
            #GPIO.output(self.PWMPin2,GPIO.LOW)
            GPIO.output(self.Pin1,GPIO.HIGH)
            GPIO.output(self.Pin2,GPIO.LOW)
            GPIO.output(self.Pin3,GPIO.HIGH)
            GPIO.output(self.Pin4,GPIO.LOW)
        elif direction=="p":
            print("receive direction=p")
            #GPIO.output(self.PWMPin,GPIO.LOW)
            #GPIO.output(self.PWMPin2,GPIO.LOW)
            GPIO.output(self.Pin1,GPIO.LOW)
            GPIO.output(self.Pin2,GPIO.LOW)
            GPIO.output(self.Pin3,GPIO.LOW)
            GPIO.output(self.Pin4,GPIO.LOW)
            print("change sectionr: ", section_r)
            self.__capture(location = section_r)
            self.status="s"

    def __speed_up(self,direction,top_speed,speed_l,speed_r):
        # top_speed=15
        # print('speed:',self.speed)
        if direction=="l" or direction=="r":
            # print('speed_l',speed_l)
            # print('speed_r',speed_r)
            # self.speed=9
            try:
                PWMfun.ChangeDutyCycle(speed_l)
                PWMfun2.ChangeDutyCycle(speed_r)
            except:
                pass
            # if direction=="l":
            #     PWMfun.ChangeDutyCycle(speed_l)
            #     PWMfun2.ChangeDutyCycle(speed_r)
            # if direction=="r":
            #     PWMfun.ChangeDutyCycle(speed_l)
            #     PWMfun2.ChangeDutyCycle(speed_r)
        else:
            if self.speed<=top_speed:
                self.speed=self.speed+2
                PWMfun.ChangeDutyCycle(self.speed)
                PWMfun2.ChangeDutyCycle(self.speed)
    def drive(self,direction="s",top_speed = 10,speed_l=5,speed_r=5,section_r='error_p'):
        if direction!=self.status:
            self.__change_direct(direction,section_r)

        else:
            if direction!="s":
                self.__speed_up(direction,top_speed,speed_l,speed_r)

    def parking(self):
        self.__slow_down()
        self.status="s"
        GPIO.output(self.Pin1,GPIO.LOW)
        GPIO.output(self.Pin2,GPIO.LOW)
        GPIO.output(self.Pin3,GPIO.LOW)
        GPIO.output(self.Pin4,GPIO.LOW)
        PWMfun.stop()
        PWMfun2.stop()
        GPIO.cleanup()

# 原本receive_motot_pwm()
def receive_photo_signal():
    ser = serial.Serial(port='/dev/ttyAMA1', baudrate=115200, timeout=0.3)
    try:
        singnal = ser.readline()
        ser.flush()
    finally:
        ser.close()
    # print('signal:',singnal)
    ser.close()
    return singnal


def job():
    global data, speed_left, speed_right, speed_top, section_r
    while(connect_status==1):
        singnal = receive_photo_signal().decode(errors='ignore')
        try:
            singnal_dict = ast.literal_eval(singnal)
            section_r = singnal_dict['section_r']

            if 'left' in singnal_dict['direction']:
                data="l"
            elif 'right' in singnal_dict['direction']:
                data="r"
            elif 'photo' in singnal_dict['direction']:
                print("receive photo signal")
                data="p"
            else:
                # if "b" in singnal_dict['direction']:
                #     data="b"
                if 'mid' in singnal_dict['direction']:
                    data="f"
                else:
                    data="s"

        # Prevent "unexpected EOF while parsing (<unknown>, line 0)" error
        except SyntaxError:
            pass

        except Exception as e:
            print("ERROR:",e)
            # pass

    GPIO.cleanup()

count = 0
time.sleep(5)
mycar=Asparagus_car()
data = "s"
speed_left = 0
speed_right = 0
speed_top = 0
connect_status = 1
section_r = 'error_p'

try:
    t = threading.Thread(target = job)
    t.start()
    while(True):
        pr_data=data
        # print(pr_data)
        # ser.write(b'A')
        mycar.drive(pr_data, top_speed=speed_top, speed_l=speed_left, speed_r=speed_right, section_r=section_r)
        time.sleep(0.1)
        count = count+1
    mycar.parking()
finally:
    mycar.parking()
    GPIO.cleanup()





