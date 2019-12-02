#-----------------------------------------------------------------------------------------
# mqtt_client v. 8/11/2019
# usa Eclipse PAHO MQTT Lib
#------------------------------------------------------------------------------------------
import paho.mqtt.client as mqtt #import module
import time
import sys
#----------------------------------------------------------------------------------------
#bridge_address="mosquitto.1544-d-iot-data-platform-1544.svc.cluster.local:1883"
bridge_address="test.mosquitto.org";
#-----------------------------------------------------------------------------------------

# Callback function per il client BRIDGE
#-----------------------------------------------------------------------------------------
def on_connect_bridge(client, userdata, flags, rc):
    if rc==0:
        print("bridgeclient connected OK")
    else:
        print("bridgeclient Bad connection=",rc)
#-----------------------------------------------------------------------------------------
def on_message_bridge(client, userdata, message):
    print("message received from BRIDGE, topic: "+message.topic+", payload: " +str(message.payload.decode("utf-8")))
#-----------------------------------------------------------------------------------------
def on_publish_bridge(client, userdata, message):
    print("Publishing message to BRIDGE, topic: "+message.topic+", payload: " +str(message.payload.decode("utf-8")))
#-----------------------------------------------------------------------------------------
print("creating bridge client")
bridgeclient = mqtt.Client("BRIDGECLIENT") #create new client instance
bridgeclient.on_message=on_message_bridge #attach messaging callback
bridgeclient.on_publish=on_publish_bridge #attach publishing callback
bridgeclient.on_connect=on_connect_bridge #attach connecting callback
print("connecting bridge client")
bridgeclient.connect(bridge_address) #connect to bridge
print("Subscribing bridgeclient to all topics")
bridgeclient.subscribe("#")  #riceve tutti i messaggi del server BRIDGE
bridgeclient.loop_start() #rimane in attesa sulla porta di connessionE
i = 1
while i < 30:
	print(i)
	i += 1
	newTopic="devices/smartpipe/messages/events/dev="+str(i);
	message = "new message #" + str(i)
	print("Messaggio che invio: " + message)
	ret= bridgeclient.publish(newTopic,str(message))
	print("messaggio inviato con risposta"+str(ret))