from django.contrib import admin

from .models import Fingerprint


@admin.register(Fingerprint)
class FingerprintAdmin(admin.ModelAdmin):
    list_display = ("template_id", "owner", "finger_type")
