# LED Server
# 
# This program runs on the Raspberry Pi and accepts requests to turn on and off
# the LED via TCP packets.

import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')

import time
import socket
from grovepi import *

def Main():

    led = 4
    pinMode(led, "OUTPUT")
    time.sleep(1)

    """127.0.0.1 is the loopback address. Any packets sent to this address will
    essentially loop right back to your machine and look for any process 
    listening in on the port specified."""
    host = '192.168.1.134'
    port = 9000

    s = socket.socket()
    s.bind((host,port))

    s.listen(1)
    c, addr = s.accept()
    print("Connection from: " + str(addr))
    
    while True:
        data = c.recv(1024).decode('utf-8')
        if not data:
            break
        print("From connected user: " + data)

        try:
            if data == "LED_ON":
                digitalWrite(led,1)		# Send HIGH to switch on LED
                print ("LED ON!")
                time.sleep(1)
            elif data == "LED_OFF":
                digitalWrite(led,0)		# Send LOW to switch off LED
                print ("LED OFF!")
                time.sleep(1)
        except KeyboardInterrupt:	# Turn LED off before stopping
            digitalWrite(led,0)
            break
        except IOError:				# Print "Error" if communication error encountered
            print ("Error")
    c.close()

"""This if-statement checks if you are running this python file directly. That 
is, if you run `python3 tcpClient.py` in terminal, this if-statement will be 
true"""
if __name__ == '__main__':
    Main()