import time
import machine
from machine import Pin
import ubinascii
from umqttsimple import MQTTClient

speed = 512
led = Pin(2, Pin.OUT)

led = machine.Pin(2, machine.Pin.OUT, value=1)
last_message = 0
message_interval = 5
counter = 0
config = {
    "server": "farmer.cloudmqtt.com",
    "port": 12487,
    "user": "lxzvqebd",
    "pswd": "M0D6C8lfFRGG",
    "pub_topic": "rccar",
    "sub_topic": "rccar"
}


def sub_cb(topic: str, msg: str) -> None:
    if topic == config['sub_topic'].encode():
        print(msg.decode())
        if 'Key.upP' in msg.decode():
            led.on()
        elif 'Key.upR' in msg.decode():
            led.off()
        elif 'Key.downP' in msg.decode():
            led.on()
        elif 'Key.downR' in msg.decode():
            led.off()
        elif 'Key.leftP' in msg.decode():
            led.on()
        elif 'Key.leftR' in msg.decode():
            led.off()
        elif 'Key.rightP' in msg.decode():
            led.on()
        elif 'Key.rightR' in msg.decode():
            led.off()
        elif 'Key.ctrlP' in msg.decode():
            set_speed(1024)
        elif 'Key.ctrlR' in msg.decode():
            set_speed(512)
        else:
            print('Message is not a command-> {}'.format(msg))

def set_speed(s):
    speed = s
    print(speed)

def connect_and_subscribe():
    client_id = ubinascii.hexlify(machine.unique_id())
    client = MQTTClient(
        client_id,
        config['server'],
        port=config['port'],
        user=config['user'],
        password=config['pswd'])
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(config['pub_topic'])
    print('Connected to %s MQTT broker, subscribed to %s topic' %
          (config['server'], config['pub_topic']))
    return client


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


try:
    client = connect_and_subscribe()
except OSError as e:
    print('Exception occured \n{}'.format(e))
    restart_and_reconnect()

while True:
    try:
        client.check_msg()
        # Publish routine
        if (time.time() - last_message) > message_interval:
            # msg = b'{}s passed'.format(counter)
            # client.publish(config['pub_topic'], msg)
            last_message = time.time()
            # counter += 5
    except OSError as e:
        restart_and_reconnect()
