"""EE 250L Lab 07 Skeleton Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time

sys.path.append('../../../Software/Python/')
from grovepie import *

led = 4
pinMode(led, "OUTPUT")


def lcd_callback(client, userdata, msg):
    print(str(msg.payload.decode("utf-8")))

def led_callback(client, userdata, msg):
    if str(msg.payload.decode("utf-8")) == "ON":
        print("turning led ON")
        digitalWrite(led, 1)
    elif str(msg.payload.decode("utf-8")) == "OFF":
        print("turning led OFF")
        digitalWrite(led, 0)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload.decode("utf-8")))

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("anrg-pi12/led")
    client.subscribe("anrg-pi12/lcd")
    client.message_callback_add("anrg-pi12/lcd", lcd_callback)
    client.message_callback_add("anrg-pi12/led", led_callback)

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)

