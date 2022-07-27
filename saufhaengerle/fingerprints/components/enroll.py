from datetime import datetime
from logging import getLogger
from typing import Optional

from django.utils.timezone import now
from django_unicorn.components import QuerySetType, UnicornView

from fingerprints.models import Fingerprint, FingerTypes
from mqtt.integrations import mqtt_client
from mqtt.models import Message, Topic
from saufhaengerle.settings import MQTT
from users.models import User

log = getLogger("fingerprints")


class EnrollView(UnicornView):
    finger_options = FingerTypes.choices
    users: QuerySetType[User] = User.objects.none()
    last_update: datetime
    finger: Optional[str] = None
    owner_username: Optional[str] = None
    messages: Optional[list[str]] = None

    def mount(self) -> None:
        self.users = User.objects.all()
        self.last_update = now()

    def enroll(self) -> None:
        if self.messages is None:
            self.messages = []

        if self.owner_username is None:
            self.messages.append("Please select an owner")
            return
        if self.finger is None:
            self.messages.append("Please select a finger")
            return

        try:
            owner = User.objects.get(username=self.owner_username)
        except User.DoesNotExist:
            self.messages.append(f"User '{self.owner_username}' does not exist")
            return

        try:
            Fingerprint.objects.get(owner=owner, finger_type=self.finger)
        except Fingerprint.DoesNotExist:
            pass
        else:
            self.messages.append(f"User '{self.owner_username}' already enrolled {self.finger}")
            return

        mqtt_client.send_message(MQTT.topics.FINGERPRINT_IN, "ENROLL")

    def get_messages(self) -> None:
        topics = Topic.objects.filter(name__in=(MQTT.topics.FINGERPRINT_DEBUG, MQTT.topics.FINGERPRINT_OUT))
        new_mqtt_messages = [
            f"[{m.created_at.strftime('%H:%M:%S')}] {m.payload}"
            for m in Message.objects.filter(topic__in=topics, created_at__gte=self.last_update).order_by("created_at")
        ]
        if self.messages:
            self.messages += new_mqtt_messages
        else:
            self.messages = new_mqtt_messages

        self.last_update = now()

    def reset_messages(self) -> None:
        self.messages = []
        self.last_update = now()

    def save(self) -> None:
        """Save the ID found in self.messages to the selected user"""
        if self.messages is None:
            self.messages = []

        if self.owner_username is None:
            self.messages.append("Please select an owner")
            return
        if self.finger is None:
            self.messages.append("Please select a finger")
            return

        try:
            owner = User.objects.get(username=self.owner_username)
        except User.DoesNotExist:
            self.messages.append(f"User '{self.owner_username}' does not exist")
            return

        for message in self.messages:
            if "Enrolled new finger at ID = " in message:
                template_id = int(message.split("=")[-1].strip())
                break
        else:
            self.messages.append(f"Failed to find template_id in messages - was the enrollment successful?")
            return

        # TODO: Fix finger_type -> need to use 'LEFT_THUMB' - not 'Left thumb'
        new_finger = Fingerprint.objects.create(owner=owner, finger_type=self.finger, template_id=template_id)
        self.messages.append(f"Successfully created {new_finger}")
