import paho.mqtt.client as mqtt
import time

broker_hostname = "eclipse.usc.edu"
broker_port = 11000

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

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
    	temp += 1
        time.sleep(0.2)