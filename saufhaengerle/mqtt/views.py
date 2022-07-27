from logging import getLogger

from django.http import HttpRequest
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from mqtt.helpers import create_lock_event, send_unlock_if_authorized, store_mqtt_message

log = getLogger("mqtt-api")
log.setLevel("DEBUG")


@require_http_methods(["POST"])
@csrf_exempt
def message(request: HttpRequest) -> HttpResponse:
    log.debug(f"Received POST: {request.POST}")

    stored = store_mqtt_message(request.POST)
    if not stored:
        return HttpResponse(status=400)

    return HttpResponse(status=200)


@require_http_methods(["POST"])
@csrf_exempt
def unlock(request: HttpRequest) -> HttpResponse:
    log.debug(f"Received POST: {request.POST}")

    stored = store_mqtt_message(request.POST)
    if not stored:
        return HttpResponse(status=500)

    _, message = stored
    if send_unlock_if_authorized(message):
        return HttpResponse(status=200)
    return HttpResponse(status=401)


@require_http_methods(["POST"])
@csrf_exempt
def lock(request: HttpRequest) -> HttpResponse:
    log.debug(f"Received POST: {request.POST}")

    if not store_mqtt_message(request.POST):
        log.error("Failed to store mqtt message")
        return HttpResponse(status=500)

    if create_lock_event():
        return HttpResponse(status=200)
    log.error("Failed to create lock event")
    return HttpResponse(status=500)
