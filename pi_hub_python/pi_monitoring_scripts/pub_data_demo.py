import paho.mqtt.client as paho
import json

# Define broker ip and port
broker="34.245.132.242"
port=1883

# Define measurment
measurement = "systemUsage"

# Define message to be called when data is pubished
def on_publish(client,userdata,result):
        print("data published \n")
        pass

# Define json data object
json_data = {
        "cpu": 50,
        "ram": 78
        }

# Create connection object
client1= paho.Client("control1")   

# Define which message is called when data is published
client1.on_publish = on_publish                        

# Connect to the broker
client1.connect(broker,port)

# Publish data to the broker. Be sure to use json.dumps to convert the json data to a string
ret= client1.publish("binBot/"+measurement, json.dumps(json_data))
