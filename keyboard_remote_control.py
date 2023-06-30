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
from rpi4motor_left import Asparagus_car

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


def main():
    mycar = Asparagus_car()
    print("Press up to speed up.")
    print("Press down to stop")
    print("Press right to turn right")
    print("Press left to turn left. \n")
    try:
        while True:
            key = getkey()
            # 要加速就多按幾下，會越來越快
            if key == keys.UP:
                print('forward')
                mycar.drive(direction="f", top_speed=20, speed_l=10, speed_r=10)

            elif key == keys.DOWN:
                print('slow down')
                mycar.drive(direction="s", speed_l=0, speed_r=0)

            elif key == keys.LEFT:
                print('turn left')
                mycar.drive(direction="l", speed_l=3, speed_r=10)

            elif key == keys.RIGHT:
                print('turn right')
                mycar.drive(direction="r", speed_l=10, speed_r=3)

    except KeyboardInterrupt:
        print("\nStop the program...")

    finally:
        print("GPIO cleaning...")
        GPIO.cleanup()

if __name__ == "__main__":
    main()