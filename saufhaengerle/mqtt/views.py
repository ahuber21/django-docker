from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Message, Topic


@require_http_methods(["POST"])
@csrf_exempt
def message(request):
    topic_name = request.POST.get("topic")
    payload = request.POST.get("payload")
    if topic_name is None or not isinstance(topic_name, str):
        return HttpResponse(status=400)
    if payload is None or not isinstance(topic_name, str):
        return HttpResponse(status=400)

    topic, _ = Topic.objects.get_or_create(name=topic_name)
    Message.objects.create(topic=topic, payload=payload)

    return HttpResponse(status=200)
