from logging import getLogger

from django.http import HttpRequest
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from actions.models import Event, EventType

log = getLogger("actions-api")


@require_http_methods(["POST"])
@csrf_exempt
def evaluate(message: HttpRequest) -> HttpResponse:
    last_unlock = Event.objects.filter(event_type=EventType.UNLOCK).last()
    last_lock = Event.objects.filter(event_type=EventType.LOCK).last()
    if last_unlock is None or last_lock is None:
        log.error("Failed to find lock and unlock events")
        return HttpResponse(status=500)
    if last_unlock.timestamp > last_lock.timestamp:
        log.error("Last unlock happened after last lock - confused")
        return HttpResponse(status=500)

    return HttpResponse(status=200)
