#Ultrasonic Sensor Server
#
# This code runs on your VM and receives a stream of packets holding ultrasonic
# sensor data and prints it to stdout. Use a UDP socket here.

import socket

    

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
ultrasonic_ranger = 4

def Process2():
    # Change the host and port as needed. For ports, use a number in the 9000 
    # range. 
    host = '192.168.1.249'
    port = 9001

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))

    print("VM Server Started")
    while True:
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print("Message From: " + str(addr))
        print("From connected pi: " + data)
    c.close()

if __name__ == '__main__':
    Process2()