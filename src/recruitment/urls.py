from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("candidato/<int:candidate_id>", views.candidate_detail, name="candidato"),
    path("candidato/criar", views.candidate_create, name="candidate_create"),
    path("candidato", views.candidate_list, name="candidate_list"),
]
