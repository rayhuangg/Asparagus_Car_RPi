# RPiCar1(2)Left:
# responsible for controlling the motors on both sides
# and capturing images on the left side.

# RPiCar1(2)Right:
# only responsible for capturing images on the right side.

import os
import socket
import time
import imageUpload as up
import RPi.GPIO as GPIO
from datetime import datetime


class AsparagusCar:
    def __init__(self):
        self.hostname = socket.gethostname()
        if self.hostname in ["RPiCar1Left", "RPiCar2Left"]:
            # Define the pin number
            self.Pin1 = 6
            self.Pin2 = 5
            self.Pin3 = 19
            self.Pin4 = 16
            self.PWMPin_left = 12
            self.PWMPin_right = 13

            # Initial the status
            self.speed = 0
            self.status = "s"  # Forward, Stop, Backword

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

            self.PWM_output_left = GPIO.PWM(self.PWMPin_left, 600)
            self.PWM_output_right = GPIO.PWM(self.PWMPin_right, 600)
            self.PWM_output_left.start(self.speed)
            self.PWM_output_right.start(self.speed)

        elif self.hostname in ["RPiCar1Right", "RPiCar2Right"]:
            self.status = "s"

        print("Car ready")


    def capture(self, section="unspecified", detection=False):
        now = datetime.now().strftime("%Y%m%d_%H_%M_%S")
        if self.hostname in ["RPiCar1Left", "RPiCar2Left"]:
            path = "photo_record/left/"
        elif self.hostname in ["RPiCar1Right", "RPiCar2Right"]:
            path = "photo_record/right/"

        if not os.path.isdir(path):
            os.makedirs(path, mode=0o777)

        if section == "unspecified":
            if self.hostname in ["RPiCar1Left", "RPiCar2Left"]:
                filename = f"{now}_left.jpg"
            elif self.hostname in ["RPiCar1Right", "RPiCar2Right"]:
                filename = f"{now}_right.jpg"
            else:
                filename = f"{now}.jpg"
        else:
            filename = f"{now}-{section}.jpg"

        # action = f"libcamera-still -n -t 1 -o {path}/{filename}" # 3280x2464
        # action = f"libcamera-still -n -t 1 -o {path}/{filename} --width 1920 --height 1080" # 1920x1080

        # This resolution prevent GPU OOM when predict on the webserver with MaskDINO
        action = f"libcamera-still -n -t 1 -o {path}/{filename} --width 1800 --height 1012"
        os.system(action)

        up.side(section=section, imagepath=f"{path}/{filename}", name=filename, detection=detection)
        time.sleep(1.2)
        print("photo saved and upload successed")

    # It not the really slow down, it's stop
    # TODO: Implement the slow down code
    def __slow_down(self):
        if self.status == "b" or self.status == "f" or self.status == "s":  # bf不確定原因
            while self.speed > 0:
                self.speed = self.speed - 3
                if self.speed < 0:
                    break
                self.PWM_output_left.ChangeDutyCycle(self.speed)
                self.PWM_output_right.ChangeDutyCycle(self.speed)
                time.sleep(0.05)
        self.speed = 0
        self.PWM_output_left.ChangeDutyCycle(self.speed)
        self.PWM_output_right.ChangeDutyCycle(self.speed)

    def __change_direct(self, direction="s", section_r="unspecified", section_l="unspecified"):
        self.status = direction
        # s means "stop"
        if direction == "s":
            self.__slow_down()
            GPIO.output(self.Pin1, GPIO.LOW)
            GPIO.output(self.Pin2, GPIO.LOW)
            GPIO.output(self.Pin3, GPIO.LOW)
            GPIO.output(self.Pin4, GPIO.LOW)

        # f means "forward"
        elif direction == "f":
            # self.__slow_down()
            GPIO.output(self.Pin1, GPIO.HIGH)
            GPIO.output(self.Pin2, GPIO.LOW)
            GPIO.output(self.Pin3, GPIO.HIGH)
            GPIO.output(self.Pin4, GPIO.LOW)

        # b means "back"
        elif direction == "b":
            self.__slow_down()
            GPIO.output(self.Pin1, GPIO.LOW)
            GPIO.output(self.Pin2, GPIO.HIGH)
            GPIO.output(self.Pin3, GPIO.LOW)
            GPIO.output(self.Pin4, GPIO.HIGH)

        # r means "Right" ahead
        elif direction == "r":
            GPIO.output(self.Pin1, GPIO.HIGH)
            GPIO.output(self.Pin2, GPIO.LOW)
            GPIO.output(self.Pin3, GPIO.HIGH)
            GPIO.output(self.Pin4, GPIO.LOW)

        # l means "Left" ahead
        elif direction == "l":
            GPIO.output(self.Pin1, GPIO.HIGH)
            GPIO.output(self.Pin2, GPIO.LOW)
            GPIO.output(self.Pin3, GPIO.HIGH)
            GPIO.output(self.Pin4, GPIO.LOW)

        # p means "Photo", p+d means "Photo & detection"
        elif direction == "p" or direction == "p+d":
            if self.hostname in ["RPiCar1Left", "RPiCar2Left"]:
                GPIO.output(self.Pin1, GPIO.LOW)
                GPIO.output(self.Pin2, GPIO.LOW)
                GPIO.output(self.Pin3, GPIO.LOW)
                GPIO.output(self.Pin4, GPIO.LOW)
                self.capture(section=section_l, detection=(direction == "p+d"))

            elif self.hostname in ["RPiCar1Right", "RPiCar2Right"]:
                self.capture(section=section_r, detection=(direction == "p+d"))

            self.status = "s"

    def __speed_up(self, direction, top_speed, speed_l, speed_r):
        # Turn right or left
        if direction == "l" or direction == "r":
            try:
                self.PWM_output_left.ChangeDutyCycle(speed_l)
                self.PWM_output_right.ChangeDutyCycle(speed_r)
            except:
                pass

        # speed adjust
        else:
            if self.speed <= top_speed:
                self.speed = self.speed + 2
                self.PWM_output_left.ChangeDutyCycle(self.speed)
                self.PWM_output_right.ChangeDutyCycle(self.speed)

    def drive(self, direction="s", top_speed=10, speed_l=5, speed_r=5, section_r="unspecified", section_l="unspecified"):
        if direction != self.status:
            self.__change_direct(direction, section_r, section_l)
        else:
            if direction != "s":
                self.__speed_up(direction, top_speed, speed_l, speed_r)

    def parking(self):
        if self.hostname in ["RPiCar1Left", "RPiCar2Left"]:
            self.__slow_down()
            self.status = "s"
            GPIO.output(self.Pin1, GPIO.LOW)
            GPIO.output(self.Pin2, GPIO.LOW)
            GPIO.output(self.Pin3, GPIO.LOW)
            GPIO.output(self.Pin4, GPIO.LOW)
            self.PWM_output_left.stop()
            self.PWM_output_right.stop()
            GPIO.cleanup()

        elif self.hostname in ["RPiCar1Right", "RPiCar2Right"]:
            pass

