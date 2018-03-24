"""EE 250L Lab 07 Skeleton Code

Run vm_publisher.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
from pynput import keyboard

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload))

def on_press(key):
    try: 
        k = key.char # single-char keys
    except: 
        k = key.name # other keys
    
    #if k == 'w':
        #client.publish("anrg-pi12/lcd", "w")
    if k == 'a':
        #print("publishing led message: ON")
        client.publish("anrg-pi12/led", "ON")
        #client.publish("anrg-pi12/lcd", "a")
    #elif k == 's':
        #client.publish("anrg-pi12/lcd", "s")
    elif k == 'd':
        #print("publishing led message: OFF")
        client.publish("anrg-pi12/led", "OFF")
        #client.publish("anrg-pi12/lcd", "d")

if __name__ == '__main__':
    #setup the keyboard event listener
    lis = keyboard.Listener(on_press=on_press)
    lis.start() # start to listen on a separate thread

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        #print("delete this line")
        time.sleep(1)
            

