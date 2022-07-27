from logging import getLogger

from django.http import HttpRequest
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from scale.models import Measurement, Scale

log = getLogger("scale-api")


@require_http_methods(["POST"])
@csrf_exempt
def log(message: HttpRequest) -> HttpResponse:
    scale, _ = Scale.objects.get_or_create(name=message.POST["name"])
    Measurement.objects.create(scale=scale, value=message.POST["kg"])

    return HttpResponse(status=200)
