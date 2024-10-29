from django.urls import path, include
from rest_framework_nested import routers
from . import views, views_apis


router_api = routers.DefaultRouter()
router_api.register(r"candidates", views_apis.CandidateViewSet)
router_api.register(r"users", views_apis.UserViewSet)
router_education_api = routers.NestedDefaultRouter(
    router_api, r"candidates", lookup="candidate"
)
router_professional_experiences_api = routers.NestedDefaultRouter(
    router_api, r"candidates", lookup="candidate"
)
router_education_api.register(
    r"educations", views_apis.EducationViewSet, basename="candidate-educations"
)
router_professional_experiences_api.register(
    r"educations",
    views_apis.ProfessionalExperienceViewSet,
    basename="candidate-professional_expereinces",
)

urlpatterns = [
    path("cadastro/", views.user_register, name="register_user"),
    path("login", views.user_login, name="user_login"),
    path("", views.index, name="index"),
    # ---------Candidate--------- #
    path("candidato/criar", views.candidate_create, name="candidate_create"),
    path(
        "candidato/",
        views.candidate_detail,
        name="candidate_detail",
    ),
    # ---------ProfessionalExperience--------- #
    path(
        "candidato/experiencia/<int:experience_id>",
        views.professional_experience_detail,
        name="professional_experience_detail",
    ),
    path(
        "candidato/experiencia/criar",
        views.professional_experience_create,
        name="professional_experience_create",
    ),
    # ---------Education--------- #
    path(
        "candidato/escolaridade/<int:education_id>",
        views.education_detail,
        name="education_detail",
    ),
    path(
        "candidato/escolaridade/criar",
        views.education_create,
        name="education_create",
    ),
    # ---------Curriculo--------- #
    path(
        "candidato/curriculo",
        views.curriculum,
        name="curriculum",
    ),
    # -----urls das Apis----- #
    path("api/", include(router_api.urls)),
    path("api/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/", include(router_education_api.urls)),
    path("api/", include(router_professional_experiences_api.urls)),
]
