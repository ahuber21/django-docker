from datetime import datetime

from django_unicorn.components import UnicornView

from fingerprints.integrations import mqtt
from fingerprints.models import FingerTypes


class EnrollView(UnicornView):
    finger_options = [str(o[1]) for o in FingerTypes.choices]
    name: str
    finger: str
    messages: list[str]
    created: datetime

    def __init__(self, *_, **kwargs) -> None:
        super().__init__(**kwargs)
        self.created = datetime.now()

    def enroll(self):
        mqtt.send_message("fingerprint_in", "ENROLL")
