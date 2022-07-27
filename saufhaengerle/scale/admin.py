from django.contrib import admin

from .models import Measurement, Scale


@admin.register(Scale)
class ScaleAdmin(admin.ModelAdmin):
    list_display = ("name", "product")


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ("value", "scale", "timestamp")
