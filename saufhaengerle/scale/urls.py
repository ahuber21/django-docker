from django.urls import path

from scale import views

urlpatterns = [path("log/", views.log, name="log-weight-api")]
