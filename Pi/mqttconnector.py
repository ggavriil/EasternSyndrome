import paho.mqtt.client as mqtt

# We should not be able to create more than 1 MQTT clients
# Otherwise we might waste resources. Therefore, this is not a class.

mqcl = mqtt.Client()
mqcl.connect("es.giorgos.io", port=1883)
mqcl.loop_start()

def publish(message):
    mqcl.publish("VirtualTopic.ESDATA", bytes(message, "utf-8"), qos=2)

def subscribe_notif(fun):
    mqcl.subscribe("VirtualTopic.ESNOTIF")
    callback_function = fun
    mqcl.on_message = fun

def publish_angle(angle):
    mqcl.publish("VirtualTopic.ESANGLE", bytes(str(angle), "utf-8"), qos=2)
