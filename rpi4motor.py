import time
import serial
import ast

def receive_motot_pwm():
    ser = serial.Serial(port='/dev/ttyS0', baudrate = 115200, timeout=0.1)
    try:
        singnal = ser.readline()   
        ser.flush()
    finally:
        ser.close()    
    print(singnal)
    ser.close()
    return singnal


if __name__ == '__main__':
    while(1):
        singnal = receive_motot_pwm().decode()
        if singnal :
            singnal_dict = ast.literal_eval(singnal)
            print(singnal_dict['right'])
        else:
            singnal_dict = {'right':0,'left':0}
            print(singnal_dict['right'])
