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


connect_status = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
PWMfun=GPIO.PWM(12,600)
PWMfun2=GPIO.PWM(13,600)


# 原本send_motor_pwm，被搞死..
def send_message_to_rpi_right(direction,section_r):
    pwm = {'direction':direction, 'section_r':section_r}
    ser = serial.Serial(
        port='/dev/ttyAMA1', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 115200,
        timeout=0.3
	)
#     ser.write(str.encode(f'{counter}\n'))s
    ser.write(bytes(str(pwm),'utf-8'))
    ser.flush()
    time.sleep(0.1)
    print(pwm)
    ser.close()


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
        now = datetime.now().strftime('%Y%m%d_%H_%M_%S')

        folder = "/home/pi/Desktop/photo_record/left/"
        if not os.path.isdir(folder):
            os.makedirs(mode=0o777)

        filename = f"{now}-{location}.jpg"
        action_left = f'libcamera-still -n -t 1 -o {folder}/{filename} --width 1920 --height 1080'
        # action_left = f'libcamera-still -n -t 1 -o {folder}/{filename}'

        # Old
        # action_right='libcamera-still -n -t 1 -o /home/pi/Desktop/photo_record/left/'+now + '.jpg --width 1920 --height 1080'
        # action_right='libcamera-still -n -t 1 -o /home/pi/Desktop/photo_record/right/'+now + '.jpg'

        os.system(action_left)
        #print(location)
        up.side(section = location , imagepath = f'{folder}/{filename}')
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
    def __change_direct(self,direction="s",section_r='error_p',section_l='error_p'):
        # self.__slow_down()
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
            #GPIO.output(self.PWMPin,GPIO.LOW)
            #GPIO.output(self.PWMPin2,GPIO.LOW)
            GPIO.output(self.Pin1,GPIO.LOW)
            GPIO.output(self.Pin2,GPIO.LOW)
            GPIO.output(self.Pin3,GPIO.LOW)
            GPIO.output(self.Pin4,GPIO.LOW)
            self.__capture(location=section_l)
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


    def drive(self,direction="s",top_speed = 10,speed_l=5,speed_r=5,section_r='E36',section_l='error_p'):
        # print(direction)
        if direction!=self.status:
            self.__change_direct(direction, section_r, section_l)

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

def receive_motot_pwm():
    ser = serial.Serial(port='/dev/ttyS0', baudrate = 115200, timeout=0.1)
    try:
        singnal = ser.readline()
        ser.flush()
    finally:
        ser.close()
    # print('signal:',singnal)
    ser.close()
    return singnal


def job():
    global data, speed_left, speed_right, speed_top, section_r, section_l
    while(connect_status==1):
        singnal = receive_motot_pwm().decode(errors='ignore')
        try:
            singnal_dict = ast.literal_eval(singnal)
            print(singnal_dict)
            data_messsage = singnal_dict['direction']
            speed_left = round(singnal_dict['left'],2)
            speed_right = round(singnal_dict['right'],2)
            speed_top = (speed_left + speed_right) / 2
            section_r = singnal_dict['section_r']
            section_l = singnal_dict['section_l']
            send_message_to_rpi_right(data_messsage,str(section_r))
           #print('message',data_messsage)
            if 'left' in singnal_dict['direction']:
                data="l"
            elif 'right' in singnal_dict['direction']:
                data="r"
            elif 'photo' in singnal_dict['direction']:
                data="p"
            else:
                # if "b" in singnal_dict['direction']:
                #     data="b"
                if 'mid' in singnal_dict['direction']:
                    data="f"
                else:
                    data="s"
        except:
            pass
    GPIO.cleanup()

count = 0
time.sleep(5)
mycar=Asparagus_car()
data = "s"
speed_left = 0
speed_right = 0
speed_top = 0
section_r = 'error_p'
section_l = 'error_p'
connect_status = 1
try:
    t = threading.Thread(target = job)
    t.start()
    while(True):
        pr_data=data
        # print(pr_data)
        # ser.write(b'A')
        mycar.drive(pr_data,top_speed = speed_top,speed_l = speed_left,speed_r = speed_right,section_r=section_r,section_l=section_l)
        # send_motor_pwm(pr_data,speed_right,speed_left,str(section_r))
        time.sleep(0.1)
        count = count+1
    mycar.parking()
finally:
    mycar.parking()
    GPIO.cleanup()





