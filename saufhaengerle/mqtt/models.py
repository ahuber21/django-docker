from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, db_index=True)
    payload = models.CharField(max_length=2000)

    def __str__(self):
        payload = self.payload[:150]
        if len(self.payload) > 150:
            payload += "..."
        if self.created_at:
            return f"[{self.created_at.strftime('%Y-%d-%m %H:%M:%S')}] {self.topic}: {payload}"
        else:
            return f"[in memory] {self.topic}: {payload}"
