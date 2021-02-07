from django.urls import path
from trade import views

urlpatterns = [
    path("", views.index, name="index"),
]
