from django.urls import path, include
from rest_framework_nested import routers
from . import views, views_apis

router_api = routers.DefaultRouter()
router_api.register(r"candidates", views_apis.CandidateViewSet)
router_api.register(r"users", views_apis.UserViewSet)
router_education_api = routers.NestedDefaultRouter(
    router_api, r"candidates", lookup="candidate"
)
router_education_api.register(
    r"educations", views_apis.EducationViewSet, basename="candidate-educations"
)


urlpatterns = [
    path("cadastro", views.user_register, name="register_user"),
    path("login", views.user_login, name="user_login"),
    path("<str:username>", views.index, name="index"),
    # ---------Candidate--------- #
    path("candidato/criar", views.candidate_create, name="candidate_create"),
    path(
        "candidato/<str:username>",
        views.candidate_detail,
        name="candidate_detail",
    ),
    path("candidato", views.candidate_list, name="candidate_list"),
    # ---------ProfessionalExperience--------- #
    path(
        "candidato/<str:candidate_username>/experiencia/<int:experience_id>",
        views.professional_experience_detail,
        name="professional_experience_detail",
    ),
    path(
        "candidato/<str:candidate_username>/experiencia/criar",
        views.professional_experience_create,
        name="professional_experience_create",
    ),
    path(
        "candidato/<str:candidate_username>/experiencia",
        views.professional_experience_list,
        name="professional_experience_list",
    ),
    # ---------Education--------- #
    path(
        "candidato/<str:candidate_username>/escolaridade/<int:education_id>",
        views.education_detail,
        name="education_detail",
    ),
    path(
        "candidato/<str:candidate_username>/escolaridade/criar",
        views.education_create,
        name="education_create",
    ),
    path(
        "candidato/<str:candidate_username>/escolaridade",
        views.education_list,
        name="education_list",
    ),
    path(
        "candidato/<str:candidate_username>/curriculo",
        views.curriculum,
        name="curriculum",
    ),
    # -----urls das Apis----- #
    path("api/", include(router_api.urls)),
    path("api/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/", include(router_education_api.urls)),
]
