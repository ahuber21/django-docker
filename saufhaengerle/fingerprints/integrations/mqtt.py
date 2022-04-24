from logging import getLogger

import paho.mqtt.client as mqtt

from saufhaengerle.settings import MQTT

log = getLogger("fingerprints")


def on_connect(client: mqtt.Client, *_) -> None:
    log.debug("MQTT connected")


def on_disconnect(client: mqtt.Client, *_) -> None:
    connect(client)


def connect(client: mqtt.Client) -> None:
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(MQTT["host"], MQTT["port"])


CLIENT = mqtt.Client()


def send_message(topic: str, message: str) -> None:
    if not CLIENT.is_connected():
        connect(CLIENT)

    CLIENT.publish(topic, message)
