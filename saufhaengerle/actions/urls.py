from django.urls import path

from actions import views

urlpatterns = [path("evaluate/", views.evaluate, name="trigger-evaluation")]
