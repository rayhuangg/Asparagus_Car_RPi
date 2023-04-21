#!/usr/bin/env python

# Copyright (c) 2019-2020, NVIDIA CORPORATION. All rights reserved.
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import RPi.GPIO as GPIO
import time

output_pins = {
    'JETSON_XAVIER': 18,
    'JETSON_NANO': 33,
    'JETSON_NX': 33,
    'CLARA_AGX_XAVIER': 18,
    'JETSON_TX2_NX': 32,
}

output_pin = 12
led_pin_1 = 5
led_pin_2 = 6

output_pin2 = 13
led_pin_3 = 16
led_pin_4 = 19
if output_pin is None:
    raise Exception('PWM not supported on this board')


def main():
    # Pin Setup:
    # Board pin-numbering scheme
    GPIO.setmode(GPIO.BCM)
    # set pin as an output pin with optional initial state of HIGH
    GPIO.setup(output_pin, GPIO.OUT)
    GPIO.setup(led_pin_1, GPIO.OUT)
    GPIO.setup(led_pin_2, GPIO.OUT)

    GPIO.setup(output_pin2, GPIO.OUT)
    GPIO.setup(led_pin_3, GPIO.OUT)
    GPIO.setup(led_pin_4, GPIO.OUT)
   

    p = GPIO.PWM(output_pin, 600)
    p2 = GPIO.PWM(output_pin2, 600)
    val = 25
    incr = 5
    p.start(val)
    p2.start(val)

    print("PWM running. Press CTRL+C to exit.")
    try:
        while True:
            p.ChangeDutyCycle(10)
            p2.ChangeDutyCycle(10)
            GPIO.output(led_pin_1, GPIO.HIGH)
            GPIO.output(led_pin_2, GPIO.LOW)
            GPIO.output(led_pin_3, GPIO.HIGH)
            GPIO.output(led_pin_4, GPIO.LOW)            
            time.sleep(10)
            p.ChangeDutyCycle(0)
            p2.ChangeDutyCycle(0)            
            time.sleep(2)
            p.ChangeDutyCycle(5)
            p2.ChangeDutyCycle(5)
            GPIO.output(led_pin_1, GPIO.LOW)
            GPIO.output(led_pin_2, GPIO.HIGH)
            GPIO.output(led_pin_3, GPIO.LOW)
            GPIO.output(led_pin_4, GPIO.HIGH)
            time.sleep(10)
            p.ChangeDutyCycle(0)
            p2.ChangeDutyCycle(0)            
            time.sleep(2)

    finally:
        p.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    main()