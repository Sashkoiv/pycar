from pynput.keyboard import Key, Listener
import time
import paho.mqtt.client as mqtt
from config import SERVER, USER, PASS, PORT, PUB_TOPIC

def on_connect( client, userdata, flags, rc):
    print ("Connected with Code :" +str(rc))
    client.subscribe('#')

client = mqtt.Client()
client.on_connect = on_connect

client.username_pw_set(USER, PASS)
client.connect(SERVER, PORT, 60)

client.loop_start()
client.publish(PUB_TOPIC, "Publish started")

def on_press(key):
    print(' {} pressed'.format(key))
    client.publish(PUB_TOPIC, "{}P".format(key))

def on_release(key):
    print(' {} release'.format(key))
    client.publish(PUB_TOPIC, '{}R'.format(key))
    if key == Key.esc:
        # Stop client and listener
        client.loop_stop()
        client.disconnect()
        return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
