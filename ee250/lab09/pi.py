import paho.mqtt.client as mqtt
import time

broker_hostname = "eclipse.usc.edu"
broker_port = 11000
led = 3

LEDon = False

import sys
sys.path.append('../../../Software/Python/')
import grovepi
from grovepi import *
from grove_rgb_lcd import *

pinMode(led, "OUTPUT")

def led_callback(client, userdata, msg):
	if ledON:
		LEDon = False
		digitalWrite(led, 1)
	else:
		LEDon = True
		digitalWrite(led, 0)

def lcd_callback(client, userdata, msg):
    setText(str(msg.payload.decode("utf-8")))

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("anrg-pi3/lcd")
    client.subscribe("anrg-pi3/led")
    client.message_callback_add("anrg-pi12/lcd", lcd_callback)
    client.message_callback_add("anrg-pi12/led", led_callback)

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    # Connect to broker and start loop    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_hostname, broker_port, 60)
    client.loop_start()

    temp = 0
    while True:
    	client.publish("anrg-pi3/temp", temp)
    	client.publish("anrg-pi3/humidity", "humid")
    	temp += 1
    	time.sleep(1)