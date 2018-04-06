import paho.mqtt.client as mqtt
import time
from enum import Enum

class Position(Enum):
    Left = 0
    Right = 1
    Middle = 2

class Movement(Enum):
    Still = 0
    Left = 1
    Right = 2

# MQTT variables
broker_hostname = "eclipse.usc.edu"
broker_port = 11000
ultrasonic_ranger1_topic = "ultrasonic_ranger1"
ultrasonic_ranger2_topic = "ultrasonic_ranger2"

# Lists holding the ultrasonic ranger sensor distance readings. Change the 
# value of MAX_LIST_LENGTH depending on how many distance samples you would 
# like to keep at any point in time.
MAX_LIST_LENGTH = 100
ranger1_dist = []
ranger2_dist = []

def prescence():
    if ranger1_dist_avg<125 or ranger2_dist_avg<125:
        return True
    else:
        return False

def ranger1_callback(client, userdata, msg):
    global ranger1_dist
    ranger1_dist.append(min(125, int(msg.payload)))
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger1_dist = ranger1_dist[-MAX_LIST_LENGTH:]
    ranger1_dist_avg = sum(ranger1_dist) / float(len(ranger1_dist))
    ranger1_slope = [j-i for i, j in zip(ranger1_dist[:-1], ranger1_dist[1:])]
    ranger1_slope_avg = sum(ranger1_slope) / float(len(ranger1_slope))

def ranger2_callback(client, userdata, msg):
    global ranger2_dist
    ranger2_dist.append(min(125, int(msg.payload)))
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger2_dist = ranger2_dist[-MAX_LIST_LENGTH:]
    ranger2_dist_avg = sum(ranger2_dist) / float(len(ranger2_dist))
    ranger2_slope = [j-i for i, j in zip(ranger2_dist[:-1], ranger2_dist[1:])]
    ranger2_slope_avg = sum(ranger2_slope) / float(len(ranger2_slope))

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(ultrasonic_ranger1_topic)
    client.message_callback_add(ultrasonic_ranger1_topic, ranger1_callback)
    client.subscribe(ultrasonic_ranger2_topic)
    client.message_callback_add(ultrasonic_ranger2_topic, ranger2_callback)

# The callback for when a PUBLISH message is received from the server.
# This should not be called.
def on_message(client, userdata, msg): 
    print(msg.topic + " " + str(msg.payload))


if __name__ == '__main__':
    # Connect to broker and start loop    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_hostname, broker_port, 60)
    client.loop_start()

    while True:
        """ You have two lists, ranger1_dist and ranger2_dist, which hold a window
        of the past MAX_LIST_LENGTH samples published by ultrasonic ranger 1
        and 2, respectively. The signals are published roughly at intervals of
        200ms, or 5 samples/second (5 Hz). The values published are the 
        distances in centimeters to the closest object. Expect values between 
        0 and 512. However, these rangers do not detect people well beyond 
        ~125cm. """
        
        # TODO: detect movement and/or position
        
        print("ranger1: " + str(ranger1_dist[-1:]) + ", ranger2: " + 
            str(ranger2_dist[-1:])) 
        
        time.sleep(0.2)