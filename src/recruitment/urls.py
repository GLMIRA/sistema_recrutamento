from django.urls import path, include
from rest_framework import routers
from . import views, views_apis

router_api = routers.DefaultRouter()
router_api.register(r"candidates", views_apis.CandidateViewSet)


urlpatterns = [
    path("", views.index, name="index"),
    path("cadastro", views.user_register, name="register_user"),
    path("login", views.user_login, name="user_login"),
    # Candidate
    path(
        "candidato/<int:candidate_id>", views.candidate_detail, name="candidato_detail"
    ),
    path("candidato/criar", views.candidate_create, name="candidate_create"),
    path("candidato", views.candidate_list, name="candidate_list"),
    # ProfessionalExperience
    path(
        "candidato/<int:candidate_id>/experiencia/<int:experience_id>",
        views.professional_experience_detail,
        name="professional_experience_detail",
    ),
    path(
        "candidato/<int:candidate_id>/experiencia/criar",
        views.professional_experience_create,
        name="professional_experience_create",
    ),
    path(
        "candidato/<candidate_id>/experiencia",
        views.professional_experience_list,
        name="professional_experience_list",
    ),
    # Education
    path(
        "candidato/<int:candidate_id>/escolaridade/<int:education_id>",
        views.education_detail,
        name="education_detail",
    ),
    path(
        "candidato/<int:candidate_id>/escolaridade/criar",
        views.education_create,
        name="education_create",
    ),
    path(
        "candidato/<int:candidate_id>/escolaridade",
        views.education_list,
        name="education_list",
    ),
    path("candidato/<int:candidate_id>/curriculo", views.curriculum, name="curriculum"),
    # -----urls das Apis----- #
    path("api/", include(router_api.urls)),
    path("api/", include("rest_framework.urls", namespace="rest_framework")),
]
