from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class FingerTypes(models.TextChoices):
    LEFT_THUMB = "LEFT_THUMB", _("Left thump")
    LEFT_INDEX = "LEFT_INDEX", _("Left index")
    LEFT_MIDDLE = "LEFT_MIDDLE", _("Left middle")
    LEFT_RING = "LEFT_RING", _("Left ring")
    LEFT_PINKY = "LEFT_PINKY", _("Left pinky")
    RIGHT_THUMB = "RIGHT_THUMB", _("Right thump")
    RIGHT_INDEX = "RIGHT_INDEX", _("Right index")
    RIGHT_MIDDLE = "RIGHT_MIDDLE", _("Right middle")
    RIGHT_RING = "RIGHT_RING", _("Right ring")
    RIGHT_PINKY = "RIGHT_PINKY", _("Right pinky")


class Fingerprint(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, help_text="The owner of the fingerprint", db_index=True)
    finger_type = models.CharField(choices=FingerTypes.choices, max_length=12)

    def __str__(self):
        return _(f"{self.owner.username}'s {self.finger_type}")
