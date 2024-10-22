from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("candidato/<int:candidate_id>", views.candidate, name="candidato"),
]
