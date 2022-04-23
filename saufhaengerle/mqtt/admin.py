from admin_auto_filters.filters import AutocompleteFilterFactory
from django.contrib import admin

from .models import Message, Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("created_at", "topic", "payload")
    list_filter = (AutocompleteFilterFactory("Topic", "topic"),)
