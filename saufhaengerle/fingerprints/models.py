from django.db import models

from users.models import User


class FingerTypes(models.TextChoices):
    LEFT_THUMB = "LEFT_THUMB", "Left thumb"
    LEFT_INDEX = "LEFT_INDEX", "Left index"
    LEFT_MIDDLE = "LEFT_MIDDLE", "Left middle"
    LEFT_RING = "LEFT_RING", "Left ring"
    LEFT_PINKY = "LEFT_PINKY", "Left pinky"
    RIGHT_THUMB = "RIGHT_THUMB", "Right thumb"
    RIGHT_INDEX = "RIGHT_INDEX", "Right index"
    RIGHT_MIDDLE = "RIGHT_MIDDLE", "Right middle"
    RIGHT_RING = "RIGHT_RING", "Right ring"
    RIGHT_PINKY = "RIGHT_PINKY", "Right pinky"


class Fingerprint(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, help_text="The owner of the fingerprint", db_index=True)
    finger_type = models.CharField(choices=FingerTypes.choices, max_length=12)
    template_id = models.IntegerField()

    def __str__(self):
        return f"{self.owner.username}'s {self.finger_type} at ID = {self.template_id}"
