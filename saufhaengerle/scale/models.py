from django.db import models


class Scale(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self) -> str:
        return self.name


class Measurement(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    scale = models.ForeignKey(Scale, db_index=True, on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self) -> str:
        return str(self.value)
