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
