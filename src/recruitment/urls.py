from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
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
]
