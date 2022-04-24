from logging import getLogger

from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Message, Topic

log = getLogger("mqtt-api")


def pretty_request(request):
    headers = ""
    for header, value in request.META.items():
        if not header.startswith("HTTP"):
            continue
        header = "-".join([h.capitalize() for h in header[5:].lower().split("_")])
        headers += "{}: {}\n".format(header, value)

    return (
        "{method} HTTP/1.1\n"
        "Content-Length: {content_length}\n"
        "Content-Type: {content_type}\n"
        "{headers}\n\n"
        "{body}"
    ).format(
        method=request.method,
        content_length=request.META["CONTENT_LENGTH"],
        content_type=request.META["CONTENT_TYPE"],
        headers=headers,
        body=request.body,
    )


@require_http_methods(["POST"])
@csrf_exempt
def message(request):
    print(pretty_request(request))
    log.info(f"Received request with payload {request.POST}")

    topic_name = request.POST.get("topic")
    payload = request.POST.get("payload")
    if topic_name is None or not isinstance(topic_name, str):
        return HttpResponse(status=400)
    if payload is None or not isinstance(topic_name, str):
        return HttpResponse(status=400)

    topic, _ = Topic.objects.get_or_create(name=topic_name)
    Message.objects.create(topic=topic, payload=payload)

    return HttpResponse(status=200)
