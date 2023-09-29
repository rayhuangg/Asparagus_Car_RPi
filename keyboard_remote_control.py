# Only can run in the left RPi, cause the motor is driven by left side RPi

import time
from datetime import datetime
import serial
import RPi.GPIO as GPIO
from getkey import getkey, keys

import imageUpload as up
from asparagus_car import AsparagusCar

def send_message_to_rpi_right(status, section_r="unspecified"):
    pwm = {"status": status, "section_r": section_r}
    ser = serial.Serial(
        port="/dev/ttyAMA1",  # Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate=115200,
        timeout=0.3,
    )
    ser.write(bytes(str(pwm), "utf-8"))
    ser.flush()
    time.sleep(0.1)
    ser.close()


def main():
    mycar = AsparagusCar()
    print("Press up to speed up.")
    print("Press down to stop")
    print("Press right to turn right")
    print("Press left to turn left. \n")
    try:
        while True:
            key = getkey()
            # 要加速就多按幾下，會越來越快
            if key == keys.UP:
                print("forward")
                mycar.drive(direction="f", top_speed=30, speed_l=15, speed_r=15)

            elif key == keys.DOWN:
                print("slow down")
                mycar.drive(direction="s", speed_l=0, speed_r=0)

            elif key == keys.LEFT:
                print("turn left")
                mycar.drive(direction="l", speed_l=1, speed_r=15)

            elif key == keys.RIGHT:
                print("turn right")
                mycar.drive(direction="r", speed_l=15, speed_r=1)

    except KeyboardInterrupt:
        print("\nStop the program...")

    finally:
        print("GPIO cleaning...")
        mycar.parking()

if __name__ == "__main__":
    main()