from django.contrib import admin

from .models import Tap


@admin.register(Tap)
class TapAdmin(admin.ModelAdmin):
    list_display = ("user", "quantity_ml", "scale", "product_name", "timestamp")
