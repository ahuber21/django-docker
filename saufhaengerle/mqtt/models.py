from django.db import models


class Message(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    topic = models.CharField(max_length=50, db_index=True)
    payload = models.CharField(max_length=2000)

    def __str__(self):
        payload = self.payload[:150]
        if len(self.payload) > 150:
            payload += "..."
        return f"[{self.created_at.strftime('%Y-%d-%m %H:%M:%S')}] {self.topic}: {payload}"
