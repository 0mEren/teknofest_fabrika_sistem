import paho.mqtt.client as mqtt
import time

class Client():
    def __init__(self, client):
        self.client = client
        

    def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"Baglanildi: {reason_code}")
        client.subscribe("test/topic")
    def on_message(self, client, userdata, msg):
        print(f"Mesaj: {msg.payload.decode()} konu:{msg.topic}")


    def setup(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        #burada hedef ip olmali
        self.client.connect("", 1883, 60)
        self.client.loop_forever()


if __name__ == '__main__':
    set_cl = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client = Client(set_cl)
    client.setup()