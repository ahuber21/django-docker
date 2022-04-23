from django.urls import path
from mqtt import views

urlpatterns = [path("message/", views.message, name="message-api")]
