import paho.mqtt.client as mqtt

mqcl = mqtt.Client()
mqcl.connect("es.giorgos.io", port=1883)
mqcl.publish("VirtualTopic.ESNOTIF", bytes("lmao", "utf-8"), qos=2)

