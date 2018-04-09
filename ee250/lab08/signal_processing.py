import paho.mqtt.client as mqtt
import time
import requests
import json
from datetime import datetime

# MQTT variables
broker_hostname = "eclipse.usc.edu"
broker_port = 11000
ultrasonic_ranger1_topic = "ultrasonic_ranger1"
ultrasonic_ranger2_topic = "ultrasonic_ranger2"

# Lists holding the ultrasonic ranger sensor distance readings. Change the 
# value of MAX_LIST_LENGTH depending on how many distance samples you would 
# like to keep at any point in time.
MAX_LIST_LENGTH = 10
ranger1_dist = []
ranger2_dist = []
ranger1_dist_avg = 0
ranger2_dist_avg = 0
ranger1_slope = []
ranger2_slope = []
ranger1_slope_avg = 0
ranger2_slope_avg = 0

def isPresent():
    if ranger1_dist_avg < 110 or ranger2_dist_avg < 110:
        return "Present"
    else:
        return "Absent"

def getPosition():
    if abs(ranger1_dist_avg - ranger2_dist_avg) < 45:
        return "Middle"
    elif ranger1_dist_avg - ranger2_dist_avg > 0:
        return "Right"
    else:
        return "Left"

def getMovement():
    if abs(ranger1_slope_avg) < 5 and abs(ranger2_slope_avg) < 5:
        return "Still"
    elif ranger1_slope_avg > 0:
        return "Moving Right"
    else:
        return "Moving Left"

def classify():
    # This header sets the HTTP request's mimetype to `application/json`. This
    # means the payload of the HTTP message will be formatted as a json ojbect
    hdr = {
        'Content-Type': 'application/json',
        'Authorization': None #not using HTTP secure
    }

    # The payload of our message starts as a simple dictionary. Before sending
    # the HTTP message, we will format this into a json object

    if isPresent():
        if getMovement() != "Still":
            payload = { 'Time': str(datetime.now()), 'Movement': getMovement() }
            print(getMovement())   
        else:
            payload = { 'Time': str(datetime.now()), 'Still -- Position': getPosition() }
            print("Still -- Position:", getPosition())

        response = requests.post("http://0.0.0.0:5000/post-event", headers = hdr,
                                data = json.dumps(payload))
        # Print the json object from the HTTP response
        # print(response.json())


def ranger1_callback(client, userdata, msg):
    global ranger1_dist
    global ranger1_dist_avg
    global ranger1_slope
    global ranger1_slope_avg
    ranger1_dist.append(min(125, float(msg.payload.decode("utf-8"))))

    if len(ranger1_dist) >= MAX_LIST_LENGTH:
        #truncate list to only have the last MAX_LIST_LENGTH values
        ranger1_dist = ranger1_dist[-MAX_LIST_LENGTH:]
        ranger1_dist_avg = sum(ranger1_dist) / float(len(ranger1_dist))
        ranger1_slope = [j-i for i, j in zip(ranger1_dist[:-1], ranger1_dist[1:])]
        ranger1_slope_avg = sum(ranger1_slope) / float(len(ranger1_slope))

def ranger2_callback(client, userdata, msg):
    global ranger2_dist
    global ranger2_dist_avg
    global ranger2_slope
    global ranger2_slope_avg
    ranger2_dist.append(min(125, float(msg.payload.decode("utf-8"))))

    if len(ranger2_dist) >= MAX_LIST_LENGTH:
        #truncate list to only have the last MAX_LIST_LENGTH values
        ranger2_dist = ranger2_dist[-MAX_LIST_LENGTH:]
        ranger2_dist_avg = sum(ranger2_dist) / float(len(ranger2_dist))
        ranger2_slope = [j-i for i, j in zip(ranger2_dist[:-1], ranger2_dist[1:])]
        ranger2_slope_avg = sum(ranger2_slope) / float(len(ranger2_slope))
        classify()

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
        
        #print("ranger1: " + str(ranger1_dist[-1:]) + ", ranger2: " + 
       #     str(ranger2_dist[-1:])) 
        
        time.sleep(0.2)