from django.urls import path
from . import views

urlpatterns = [
    path("ask/", views.ask, name="ask"),
    path("pusher/auth/", views.pusher_auth, name="pusher_auth"),
]
