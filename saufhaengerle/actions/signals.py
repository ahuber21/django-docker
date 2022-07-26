from actions.models import Event, EventType
from django.db.models.signals import post_save
from django.dispatch import receiver
from mqtt.integrations import mqtt_client

from saufhaengerle.settings import MQTT


@receiver(post_save, sender=Event)
def event_create_callback(sender: Any, instance: Event, **_: Any) -> None:
    if instance.event_type == EventType.UNLOCK:
        finger = event.finger.finger_type if event.finger else "NO_FINGER"
        mqtt_client.send_message(
            MQTT.topics.UNLOCK, f"{instance.initiator.first_name or instance.initiator.username} | {finger}"
        )
