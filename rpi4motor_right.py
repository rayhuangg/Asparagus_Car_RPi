# -*- coding : utf-8-*-

import ast
import os
import serial
import sys
import time
import threading
import imageUpload as up
from datetime import datetime
from asparagus_car import AsparagusCar

connect_status = 0

def receive_rpi_signal():
    ser = serial.Serial(port='/dev/ttyAMA1', baudrate=115200, timeout=0.3)
    try:
        signal = ser.readline()
        ser.flush()
    finally:
        ser.close()
    ser.close()
    return signal


def job():
    global data, speed_left, speed_right, speed_top, section_r, section_l
    while connect_status == 1:
        signal = receive_rpi_signal().decode(errors='ignore')
        try:
            signal_dict = ast.literal_eval(signal)
            print(f"Received: {signal_dict}")
            data_messsage = signal_dict['direction']
            section_r = signal_dict['section_r']

            if 'photo' in data_messsage:
                print("receive photo signal")
                data = "p"
            else:
                data = "s"

        # Prevent "unexpected EOF while parsing (<unknown>, line 0)" error
        except SyntaxError:
            pass

        except Exception as e:
            print("Exception:", e)
            pass


def main():
    global connect_status
    global data, speed_left, speed_right, speed_top, section_r, section_l
    time.sleep(2)
    mycar = AsparagusCar()
    data = "s"
    speed_left = 0
    speed_right = 0
    speed_top = 0
    section_r = 'unspecified'
    section_l = 'unspecified'
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
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Program stopping...")
        connect_status = 0
        t.join()  # 等待子執行緒結束
        sys.exit()

    finally:
        print("GPIO cleaning...")
        mycar.parking()


if __name__ == "__main__":
    main()