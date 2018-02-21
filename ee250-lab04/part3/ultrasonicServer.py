#Ultrasonic Sensor Server
#
# This code runs on your VM and receives a stream of packets holding ultrasonic
# sensor data and prints it to stdout. Use a UDP socket here.

import grovepi
import socket

    

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
ultrasonic_ranger = 4

def Process2():
    # Change the host and port as needed. For ports, use a number in the 9000 
    # range. 
    host = '127.0.0.1'
    port = 9000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))

    print("VM Server Started")
    while True:

    try:
        # Read distance value from Ultrasonic
        sensorData = grovepi.ultrasonicRead(ultrasonic_ranger)

    except TypeError:
        print ("Error")
    except IOError:
        print ("Error")

        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print("Message From: " + str(addr))
        print("From connected pi: " + data)
    c.close()

if __name__ == '__main__':
    Process2()