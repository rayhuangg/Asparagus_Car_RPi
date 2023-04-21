import time
import serial

counter = 'hello im rpi4'
while True:
    ser = serial.Serial(
    port='/dev/ttyAMA0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
    baudrate = 115200,
    timeout=0.1
	)
#     ser.write(str.encode(f'{counter}\n'))s
    counter = ser.readline()
    print(counter)
    ser.write(str(counter).encode())
    time.sleep(1)
    print(counter) 
    ser.close()

    

#     counter += 1
    