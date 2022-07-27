from django.urls import path

from mqtt import views

urlpatterns = [
    path("message/", views.message, name="message-api"),
    path("unlock/", views.unlock, name="unlock-api"),
    path("lock/", views.lock, name="lock-api"),
]
