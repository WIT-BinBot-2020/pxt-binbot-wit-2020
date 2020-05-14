import paho.mqtt.client as paho
import json

# Define broker ip and port
broker="52.19.82.33"
port=1883

# Define message to be called when data is pubished
def on_publish(client,userdata,result):
        print("data published \n")
        pass


def publish(measurement, json_data):

    # Create connection object
    client1= paho.Client("control1")   

    # Define which message is called when data is published
    client1.on_publish = on_publish                        
	
    # Connect to the broker
    client1.connect(broker,port)

    # Publish data to the broker. Be sure to use json.dumps to convert the json data to a string
    ret= client1.publish("binBot/"+measurement, json.dumps(json_data))
    
    print("Disconnecting")
    client1.disconnect()

# Test Code - Uncomment for testing
"""
data = {
    "cpu": 50,
    "ram": 76
    }

publish("systemUsage", data)
"""

