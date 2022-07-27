import re
from logging import getLogger
from typing import Any, Optional, Tuple

from actions.models import Event, EventType
from fingerprints.models import Fingerprint
from mqtt.integrations import mqtt_client
from saufhaengerle.settings import MQTT

from .models import Message, Topic

re_user_id_score = re.compile(r"ID = (\d+) \| score = (\d+)")
log = getLogger("mqtt-api")


def get_fingerprint_from_id(template_id: int) -> Optional[Fingerprint]:
    # find the finger to that template_id
    try:
        return Fingerprint.objects.get(template_id=template_id)
    except Fingerprint.DoesNotExist:
        log.warning(f"No fingerprint found for {template_id=}")
        mqtt_client.send_message(MQTT.topics.ERROR, f"No fingerprint found for {template_id=}")


def store_mqtt_message(post: dict[str, Any]) -> Optional[Tuple[Topic, Message]]:
    topic_name = post.get("topic")
    payload = post.get("payload")
    if topic_name is None or not isinstance(topic_name, str):
        return None
    if payload is None or not isinstance(payload, str):
        return None

    topic, _ = Topic.objects.get_or_create(name=topic_name)
    message = Message.objects.create(topic=topic, payload=payload)

    return topic, message


def send_unlock_if_authorized(message: Message) -> bool:
    if match := re_user_id_score.search(message.payload):  # type: ignore
        # extract user id from MQTT message payload
        template_id, _ = map(int, match.groups())

        finger = get_fingerprint_from_id(template_id)
        if not finger:
            return False

        # create unlock event
        Event.objects.create(event_type=EventType.UNLOCK, initiator=finger.owner)  # type: ignore
        mqtt_client.send_message(
            MQTT.topics.UNLOCK, f"{finger.owner.first_name or finger.owner.username} | {finger.finger_type}"  # type: ignore
        )

        return True
    return False


def create_lock_event() -> bool:
    last_unlock = Event.objects.filter(event_type=EventType.UNLOCK).last()
    if last_unlock is None:
        log.error("Failed to find last_unlock")
        return False
    Event.objects.create(event_type=EventType.LOCK, initiator=last_unlock.initiator)

    return True
