import paho.mqtt.client as mqtt

mqcl = mqtt.Client()
mqcl.connect("es.giorgos.io", port=1883)

def publish(message):
    mqcl.publish("VirtualTopic.ESDATA", bytes(message, "utf-8"), qos=2)


