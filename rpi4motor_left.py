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

connect_status = False

def receive_motor_pwm():
    ser = serial.Serial(port="/dev/ttyS0", baudrate=115200, timeout=0.1)
    try:
        signal = ser.readline()
        ser.flush()
    finally:
        ser.close()
    ser.close()
    return signal


def send_message_to_rpi_right(status, section_r, detection=False):
    pwm = {"status": status, "section_r": section_r, "detection":detection}
    print("send message:", pwm)
    ser = serial.Serial(
        port="/dev/ttyAMA1",
        baudrate=115200,
        timeout=0.3,
    )
    ser.write(bytes(str(pwm), "utf-8"))
    ser.flush()
    time.sleep(0.1)
    ser.close()


def job():
    global data, speed_left, speed_right, speed_top, section_r, section_l, detection
    while connect_status:
        signal = receive_motor_pwm().decode(errors="ignore")
        try:
            signal_dict = ast.literal_eval(signal)
            print(f"Received: {signal_dict}")
            status = signal_dict["status"]
            speed_left = round(signal_dict["left"], 2)
            speed_right = round(signal_dict["right"], 2)
            speed_top = (speed_left + speed_right) / 2
            section_r = signal_dict["section_r"]
            section_l = signal_dict["section_l"]
            detection = signal_dict["detection"]

            # "data" means the status that the car should do
            # (but I think should be change to use the raw receive data)
            if "left" in status:
                data = "l"
            elif "right" in status:
                data = "r"
            elif "photo" in status:
                # "p" means take photo
                # "p+d" means take photo and to the detection immediately
                data = "p+d" if detection==True else "p"
            elif "mid" in status:
                data = "f"
            else:
                data = "s"
            time.sleep(0.1)
            send_message_to_rpi_right(status, str(section_r), detection=detection)

        # Prevent "unexpected EOF while parsing (<unknown>, line 0)" error
        except SyntaxError:
            # print("SyntaxError")
            pass

        except Exception as e:
            print("Exception:", e)


def main():
    global connect_status
    global data, speed_left, speed_right, speed_top, section_r, section_l
    time.sleep(2)
    mycar = AsparagusCar()
    data = "s"
    speed_left = 0
    speed_right = 0
    speed_top = 0
    section_r = "unspecified"
    section_l = "unspecified"
    connect_status = True
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