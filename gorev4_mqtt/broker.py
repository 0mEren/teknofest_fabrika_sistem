import paho.mqtt.client as mqtt
import time

class Broker():
    def __init__(self, client):
       self.client = client
       

    def setup(self):
        self.client.connect("localhost", 1883, 60)
        self.client.loop_start()
        try:
            while True:
                msg = "TEST"
                self.client.publish("test/topic", msg, qos =1)
                time.sleep(5)
        except KeyboardInterrupt:
            print("Interrupt")
        finally:
            self.client.loop_stop()
            self.client.disconnect()




if __name__ == '__main__':
    set_cl = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client = Broker(set_cl)
    client.setup()