import paho.mqtt.client as mqtt
import time
import sys
from datetime import datetime
import requests

gracz2 = sys.argv[1]
uuid_priv = sys.argv[2]


def on_connect(client, userdata, flags, rc):
    print("Połączono")


def on_message(client, userdata, message):
    global FLAG
    global chat
    if str(message.topic) != pubtop:
        msg = str(message.payload.decode("utf-8"))
        print(f"[{gracz2}][{datetime.now().strftime('%H:%M:%S')}]", msg)
        url = f"http://localhost:5000/games/{uuid_priv}/mqtt_backup"
        patch = {"nowy": f"[{gracz2}][{datetime.now().strftime('%H:%M:%S')}]{msg}"}
        requests.patch(url, json=patch)
        if msg == "Stop" or msg == "stop":
            FLAG = False
        else:
            chat = input("Twoja wiadomość: ")
            client.publish(pubtop, chat)


def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Zasubskrybowano: {uuid_priv}")
    url = f"http://localhost:5000/games/{uuid_priv}/0/mqtt_backup"
    if requests.get(url).status_code == 200:
        a = requests.get(url)
        for i in range(1, len(a.json())):
            print(a.json()[i]+"\n")
    else:
        pass


def on_unsubscirbe(client, userdata, mid):
    print(f"Odsubskrybowano: {uuid_priv}")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Rozłączono")


broker_address = "localhost"
port = 1883

client = mqtt.Client()
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscirbe
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port)

time.sleep(1)

pubtop = f"/chat/{uuid_priv}/1"
subtop = f"/chat/{uuid_priv}/2"
FLAG = True

client.loop_start()
client.subscribe(subtop)

time.sleep(1)
chat = input("Twoja wiadomość: ")
client.publish(pubtop, chat)
while True:
    if FLAG == False or chat == "Stop" or chat == "stop":
        break

client.disconnect()
client.loop_stop()
