from dataclasses import dataclass
from logging import getLogger
from typing import Any, Optional

from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from actions.models import Event, EventType
from scale.models import Measurement, Scale
from taps.models import Tap

log = getLogger("actions-api")


@dataclass
class MaximumDifference:
    scale: Optional[Scale] = None
    diff: float = 0
    start_measurement: Optional[Measurement] = None
    stop_measurement: Optional[Measurement] = None


@require_http_methods(["GET"])
@csrf_exempt
def evaluate(*_: Any) -> HttpResponse:
    last_unlock = Event.objects.filter(event_type=EventType.UNLOCK).last()
    last_lock = Event.objects.filter(event_type=EventType.LOCK).last()
    if last_unlock is None or last_lock is None:
        log.error("Failed to find lock and unlock events")
        return HttpResponse(status=500)
    if last_unlock.timestamp > last_lock.timestamp:
        log.error("Last unlock happened after last lock - confused")
        return HttpResponse(status=500)

    all_scales = Scale.objects.all()

    max_diff = MaximumDifference()

    for scale in all_scales:
        # get the first measurement after last_unlock
        first = (
            Measurement.objects.filter(timestamp__gte=last_unlock.timestamp, scale=scale).order_by("timestamp").first()
        )
        # get the last measurement before last_lock
        last = Measurement.objects.filter(timestamp__lte=last_lock.timestamp, scale=scale).order_by("timestamp").last()

        if first is None or last is None:
            continue

        if (diff := first.value - last.value) > max_diff.diff or max_diff.scale is None:
            max_diff.scale = scale
            max_diff.diff = diff
            max_diff.start_measurement = first
            max_diff.stop_measurement = last

    if max_diff.scale is None:
        log.error("Failed to get first / last measurements")
        return HttpResponse(status=500)

    Tap.objects.create(
        user=last_unlock.initiator,
        unlock=last_unlock,
        lock=last_lock,
        start_measurement=max_diff.start_measurement,
        stop_measurement=max_diff.stop_measurement,
        quantity_ml=(1000.0 * max_diff.diff),
    )

    return HttpResponse(status=200)
