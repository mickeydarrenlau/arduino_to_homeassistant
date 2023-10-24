import paho.mqtt.client as mqtt
from pyfirmata import Arduino, util
board = Arduino('COM8')
import pyfirmata
import private
import json
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")
    
    data_1 = {
  "~": "homeassistant/light/arduino-1-first-led",
  "name": "Arduino First Led",
  "uniq_id": "arduino-1-first-led",
  "cmd_t": "~/set",
  "stat_t": "~/state",
  "schema": "json",
  "dev": {
    "ids": "arduino-1",
    "name": "Arduino",
    "mf": "Pyfirmata",
    "mdl": "Arduino",
    "sw": "1.0",
    "hw": "1.0rev2",
  },
  "o": {
    "name":"Pyfirmata",
    "sw": "2.1",
  }
}
    
    data_2 = {
  "~": "homeassistant/binary_sensor/arduino-1-first-button",
  "name": "Arduino First Button",
  "uniq_id": "arduino-1-first-button",
  "stat_t": "~/state",
  "schema": "json",
  "dev": {
    "ids": "arduino-1",
    "name": "Arduino",
    "mf": "Pyfirmata",
    "mdl": "Arduino",
    "sw": "1.0",
    "hw": "1.0rev2",
  },
  "o": {
    "name":"Pyfirmata",
    "sw": "2.1",
  }
}
    
    data_3 = {
  "~": "homeassistant/binary_sensor/arduino-1-first-ir",
  "name": "Arduino First IR Sensor",
  "uniq_id": "arduino-1-first-ir",
  "stat_t": "~/state",
  "schema": "json",
  "dev": {
    "ids": "arduino-1",
    "name": "Arduino",
    "mf": "Pyfirmata",
    "mdl": "Arduino",
    "sw": "1.0",
    "hw": "1.0rev2",
  },
  "o": {
    "name":"Pyfirmata",
    "sw": "2.1",
  }
}

    client.publish("homeassistant/light/arduino-1-first-led/config", payload=json.dumps(data_1))
    client.publish("homeassistant/binary_sensor/arduino-1-first-button/config", payload=json.dumps(data_2))
    client.publish("homeassistant/binary_sensor/arduino-1-first-ir/config", payload=json.dumps(data_3))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic, msg.payload)
    pass

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def on_first_led_set(client, userdata, msg):
    data_json = json.loads(msg.payload)
    if data_json["state"] == "ON":
        board.digital[12].write(1)
        client.publish("homeassistant/light/arduino-1-first-led/state", payload=json.dumps(data_json), retain=True)
    else:
        board.digital[12].write(0)
        client.publish("homeassistant/light/arduino-1-first-led/state", payload=json.dumps(data_json), retain=True)

def on_first_led_state_recover(client, userdata, msg):
    data_json = json.loads(msg.payload)
    if data_json["state"] == "ON":
        board.digital[12].write(1)

    else:
        board.digital[12].write(0)


client.tls_set('./mqtt.crt')
client.message_callback_add("homeassistant/light/arduino-1-first-led/set", on_first_led_set)
client.message_callback_add("homeassistant/light/arduino-1-first-led/state", on_first_led_state_recover)
client.username_pw_set(private.mqtt_username, password=private.mqtt_password)
client.connect(private.mqtt_broker, private.mqtt_port, 60)

client.loop_start()
it = pyfirmata.util.Iterator(board)
it.start()

board.digital[8].mode = pyfirmata.INPUT
board.digital[11].mode = pyfirmata.INPUT

while True:
    sw1 = board.digital[8].read()
    sw2 = board.digital[11].read()
    if sw1 is True:
        client.publish("homeassistant/binary_sensor/arduino-1-first-button/state", payload="ON")
    else:
        client.publish("homeassistant/binary_sensor/arduino-1-first-button/state", payload="OFF")
    if sw2 is False:
        client.publish("homeassistant/binary_sensor/arduino-1-first-ir/state", payload="ON")
    else:
        client.publish("homeassistant/binary_sensor/arduino-1-first-ir/state", payload="OFF")
    time.sleep(0.5)
