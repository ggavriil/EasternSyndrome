import paho.mqtt.client as mqtt

mqcl = mqtt.Client()
mqcl.connect("es.giorgos.io", port=1883)
mqcl.loop_start()


def publish(message):
    mqcl.publish("VirtualTopic.ESDATA", bytes(message, "utf-8"), qos=2)

def publish_angle(angle):
    mqcl.publish("VirtualTopic.ESANGLE", bytes(str(angle), "utf-8"), qos=2)
