#-----------------------------------------------------------------------------------------
# mqtt_client v. 8/11/2019
# usa Eclipse PAHO MQTT Lib
# Legge da SMARTPIPE MQTT server e scrive su BRIDGE MQTT server
#------------------------------------------------------------------------------------------
import paho.mqtt.client as mqtt #import module
import time
import sys
#----------------------------------------------------------------------------------------
bridge_address="XX.XXX.XX.XXX"
pipe_address="YY.YYY.YY.YYY"
#-----------------------------------------------------------------------------------------
# Callback function per il client SMARTPIPE
#
def on_message_pipe(client, userdata, message):
    print("message received from SMARTPIPE, topic: "+message.topic+", payload: " +str(message.payload.decode("utf-8")))
    splitTopic = message.topic.split("/")
    newTopic="devices/smartpipe/messages/events/dev="+splitTopic[1];
    ret= bridgeclient.publish(newTopic,str(message.payload.decode("utf-8")))
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
#----------------------------------------------------------------------------------------
print("creating bridge client")
bridgeclient = mqtt.Client("BRIDGECLIENT") #create new client instance
bridgeclient.on_message=on_message_bridge #attach messaging callback
bridgeclient.on_publish=on_publish_bridge #attach publishing callback
bridgeclient.on_connect=on_connect_bridge #attach connecting callback
print("connecting bridge client")
bridgeclient.connect(bridge_address) #connect to bridge
print("Subscribing bridgeclient to all topics")
bridgeclient.subscribe("#")  #riceve tutti i messaggi del server BRIDGE
bridgeclient.loop_start() #rimane in attesa sulla porta di connessione
#----------------------------------------------------------------------------------------
print("creating smartpipe client")
pipeclient = mqtt.Client("PIPECLIENT") #create new instance
pipeclient.on_message=on_message_pipe #attach messaging callback for pipeclient
print("connecting smartpipe client")
pipeclient.connect(pipe_address) #connect to pipe broker
print("Subscribing pipeclient to smartpipe/# topics")
pipeclient.subscribe("smartpipe/#") #riceve dalla coda smartpipe solo i messaggi del tipo smartpipe/xxxx
pipeclient.loop_start()
