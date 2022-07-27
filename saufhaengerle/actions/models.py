from django.db import models

from fingerprints.models import Fingerprint
from users.models import User


class EventType(models.TextChoices):
    LOCK = ("lock", "lock")
    UNLOCK = ("unlock", "unlock")


class Event(models.Model):
    initiator = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    finger = models.ForeignKey(Fingerprint, db_index=True, null=True, on_delete=models.CASCADE)
    event_type = models.CharField(choices=EventType.choices, max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name = "UNKNOWN" if not self.initiator else (self.initiator.first_name or self.initiator.username)
        return f"{self.event_type} by {name} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
