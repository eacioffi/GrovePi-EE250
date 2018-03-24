"""EE 250L Lab 07 Skeleton Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# GPIO config
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


def lcd_callback(client, userdata, msg):
    print(str(msg.payload.decode("utf-8")))

def led_callback(client, userdata, msg):
    if str(msg.payload.decode("utf-8")) == "ON":
        print("turning led ON")
        GPIO.output(11, True)
    elif str(msg.payload.decode("utf-8")) == "OFF":
        print("turning led OFF")
        GPIO.output(11, False)

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("anrg-pi12/led")
    client.subscribe("anrg-pi12/lcd")
    client.message_callback_add("anrg-pi12/lcd", lcd_callback)
    client.message_callback_add("anrg-pi12/led", led_callback)

def on_press(key):
if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        print("delete this line")
        time.sleep(1)
            

