from django.shortcuts import HttpResponse
from django.views.decorators.http import require_http_methods

from .models import Message


@require_http_methods(["POST"])
def message(request):
    topic = request.POST.get("topic")
    payload = request.POST.get("payload")
    if topic is None or not isinstance(topic, str):
        return HttpResponse(status=400)
    if payload is None or not isinstance(topic, str):
        return HttpResponse(status=400)

    Message.objects.create(topic=topic, payload=payload)

    return HttpResponse(status=200)
