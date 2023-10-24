# -*- coding : utf-8-*-

import socket
import time
from getkey import getkey
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
                if hostname == "RPiCar1Left" or hostname == "RPiCar2Left":
                    mycar.capture(section="unspecified")
                elif hostname == "RPiCar1Right" or hostname == "RPiCar2Right":
                    mycar.capture(section="unspecified")

    except KeyboardInterrupt:
        print("Cleaning the GPIO pin.")
        mycar.parking()
        time.sleep(0.5)
        print("Bye.")