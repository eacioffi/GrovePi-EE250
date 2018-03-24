"""EE 250L Lab 07 Skeleton Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time

import sys
sys.path.append('../../../Software/Python/')
import grovepi
from grovepi import *

if sys.platform == 'uwp':
    import winrt_smbus as smbus
    bus = smbus.SMBus(1)
else:
    import smbus
    import RPi.GPIO as GPIO
    rev = GPIO.RPI_REVISION
    if rev == 2 or rev == 3:
        bus = smbus.SMBus(1)
    else:
        bus = smbus.SMBus(0)

# this device has two I2C addresses
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

# set backlight to (R,G,B) (values from 0..255 for each)
def setRGB(r,g,b):
    bus.write_byte_data(DISPLAY_RGB_ADDR,0,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,1,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR,4,r)
    bus.write_byte_data(DISPLAY_RGB_ADDR,3,g)
    bus.write_byte_data(DISPLAY_RGB_ADDR,2,b)

# send command to display (no need for external use)    
def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

# set display text \n for second line(or auto wrap)     
def setText(text):
    textCommand(0x01) # clear display
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

#Update the display without erasing the display
def setText_norefresh(text):
    textCommand(0x02) # return home
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    while len(text) < 32: #clears the rest of the screen
        text += ' '
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

led = 4
pinMode(led, "OUTPUT")

def lcd_callback(client, userdata, msg):
    #setText(str(msg.payload.decode("utf-8")))
    setText("test")

def led_callback(client, userdata, msg):
    if str(msg.payload.decode("utf-8")) == "ON":
        #print("turning led ON")
        digitalWrite(led, 1)
    elif str(msg.payload.decode("utf-8")) == "OFF":
        #print("turning led OFF")
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
        data = grovepi.ultrasonicRead(3)
        client.publish("anrg-pi12/usRanger", str(data).encode('utf-8')) 

