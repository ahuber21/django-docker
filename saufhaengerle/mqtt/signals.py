import re
from logging import getLogger
from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver
from fingerprints.models import Fingerprint
from mqtt.integrations import mqtt_client
from mqtt.models import Message

from saufhaengerle.settings import MQTT

log = getLogger("mqtt-api")

re_user_id_score = re.compile(r"ID = (\d+) \| score = (\d+)")


@receiver(post_save, sender=Message)
def message_create_callback(sender: Any, instance: Message, **_: Any) -> None:
    log.info(f"MQTT message callback triggered by: {sender} / {instance}")
    topic = str(instance.topic)
    if topic == MQTT.topics.FINGERPRINT_OUT:
        __handle_fingerprint_out_message(instance)
    else:
        log.info(f"Ignoring message on topic '{topic}'")


def __handle_fingerprint_out_message(message: Message) -> None:
    if match := re_user_id_score.search(message.payload):
        # extract user id from MQTT message payload
        template_id, _ = map(int, match.groups())

        # find the finger to that template_id
        try:
            finger = Fingerprint.objects.get(template_id=template_id)
        except Fingerprint.DoesNotExist:
            log.warning(f"No fingerprint found for {template_id=}")
            mqtt_client.send_message("saufhaengerle/error", f"No fingerprint found for {template_id=}")
            return

        mqtt_client.send_message(
            "saufhaengerle/unlock", f"{finger.owner.first_name or finger.owner.username} | {finger.finger_type}"
        )
