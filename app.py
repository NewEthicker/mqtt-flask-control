from umqtt import MQTTClient

client = MQTTClient("ec200u", "yamanote.proxy.rlwy.net", 1883)
client.connect()
client.publish("counter", '{"counter":42}')
client.disconnect()
