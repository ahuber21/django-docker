from django.test import TestCase
from django.urls import reverse

from .models import Message


class MessageApiTests(TestCase):
    database = {"default"}

    def test_post_response(self):
        response = self.client.post(reverse("message-api"), data={"topic": "foo", "payload": "bar"})
        self.assertEqual(response.status_code, 200)

    def test_broken_payload(self):
        response = self.client.post(reverse("message-api"), data={})
        self.assertEqual(response.status_code, 400)

    def test_wrong_request_type(self):
        response = self.client.get(reverse("message-api"))
        self.assertEqual(response.status_code, 405)

    def test_message_created_with_correct_request(self):
        n_before = Message.objects.all().count()
        self.client.post(reverse("message-api"), data={"topic": "foo", "payload": "bar"})
        n_after = Message.objects.all().count()
        self.assertEqual(n_after, n_before + 1)
