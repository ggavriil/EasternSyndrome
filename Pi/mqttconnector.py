import paho.mqtt.client as mqtt

mqcl = mqtt.Client()
#mqcl.connect("es.giorgos.io", port=1833)
def connectToServer(client, userdata, rc):
    mqcl.connect("es.giorgos.io", port=1833)

#connectToServer(None, None, None)


#mqcl.on_disconnet = connectToServer
def publish(message):
    mqcl.publish("VirtualTopic.ESDATA", bytes(message, "utf-8"), qos=2)


