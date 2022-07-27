from django.db import models

from actions.models import Event
from scale.models import Measurement, Scale
from users.models import User


class Tap(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    unlock = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="unlock_event")
    lock = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="lock_event")
    start_measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE, related_name="start_measurement")
    stop_measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE, related_name="stop_measurement")
    scale = models.ForeignKey(Scale, null=True, on_delete=models.SET_NULL)
    quantity_ml = models.FloatField()
    product_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.user}: {self.quantity_ml} ml"
