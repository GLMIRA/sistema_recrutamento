from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpRequest
from django.template import loader
from .models import Candidate, ProfessionalExperience, Education
from .forms import (
    CandidateForm,
    ProfessionalExperienceForm,
    EducationForm,
    UserForm,
    LoginForm,
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test


def staff_required(user):
    return user.is_staff


def user_register(request: HttpRequest):
    """"""
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Não salva ainda no banco
            user.set_password(form.cleaned_data["password"])
            form.save()
            return redirect("user_login")
    else:
        form = UserForm()

    return render(request, "recruitiment/user_register.html", {"form": form})


def user_login(request: HttpRequest):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                print("entrei aqui")
                login(request, user)
                return redirect("index")
            else:
                print("entrei_aqui_2")
                form.add_error(None, "usuario ou senha invalidos")
    else:
        form = LoginForm()

    return render(request, "recruitiment/user_login.html", {"form": form})


@login_required(login_url="user_login")
def index(request):
    if request.method == "POST":
        return redirect(f"/recruitment/candidato/criar")
    return render(request, "recruitiment/index_template.html")


# Candidatos
@login_required(login_url="user_login")
def candidate_detail(request: HttpRequest, candidate_id: int) -> HttpResponse:
    """funaço para editar candiadto

    Args:
        request (HttpRequest): tipo requisiçao(POST,GET)
        candidate_id (int): id candidato

    Returns:
        HttpResponse: Redireciona para a página inicial após salvar ou
        renderiza o template com o formulário preenchido para edição.
    """
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == "POST":
        form = CandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            return redirect(f"/recruitment/candidato/{candidate.id}/curriculo")
    else:
        form = CandidateForm(instance=candidate)
    return render(
        request,
        "recruitiment/candidate_detail.html",
        {"form": form, "candidate": candidate},
    )


@login_required(login_url="user_login")
def candidate_create(request: HttpRequest) -> HttpResponse:
    """funaço para criar candiadto

    Args:
        request (HttpRequest): tipo requisiçao(POST,GET)

    Returns:
        HttpResponse: Redireciona para a página inicial após salvar ou
        renderiza o template com o formulário vazio para criacao.
    """
    if request.method == "POST":
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save()
            return redirect(f"/recruitment/candidato/{candidate.id}/curriculo")
    else:
        form = CandidateForm()
    return render(request, "recruitiment/candidate_create.html", {"form": form})


@login_required(login_url="user_login")
@user_passes_test(staff_required)
def candidate_list(request: HttpRequest) -> HttpResponse:
    """Lista todos os Candidatos

    Args:
        request (HttpRequest): Requisição HTTP, (GET)

    Returns:
        HttpResponse: Lista todos candidatos cadastrados
    """
    candidates = get_list_or_404(Candidate)
    return render(
        request, "recruitiment/candidate_list.html", {"candidates": candidates}
    )


# Parte Profisional
@login_required(login_url="user_login")
def professional_experience_detail(
    request: HttpRequest, candidate_id: int, experience_id: int
):
    """Função para visualizar detalhes de uma experiência profissional
        de um candidato.

    Args:
        request (HttpRequest): A requisição HTTP.
        candidate_id (int): O ID do candidato.
        professional_id (int): O ID da experiência profissional.

    Returns:
        HttpResponse: Redireciona a pagian inicial ou
        reenderiza o template com os detalhes da
        experiência profissional.
    """
    candidate = get_object_or_404(Candidate, id=candidate_id)
    professional_experience = get_object_or_404(
        ProfessionalExperience, id=experience_id, candidate=candidate
    )
    if request.method == "POST":
        form = ProfessionalExperienceForm(
            request.POST, instance=professional_experience
        )
        if form.is_valid():
            form.save()
            return redirect(f"/recruitment/candidato/{candidate.id}/curriculo")
    else:
        form = ProfessionalExperienceForm(instance=professional_experience)
    return render(
        request,
        "recruitiment/professional_experience_detail.html",
        {
            "form": form,
            "professional_experience": professional_experience,
            "candidate": candidate,
        },
    )


@login_required(login_url="user_login")
def professional_experience_create(
    request: HttpRequest, candidate_id: int
) -> HttpResponse:
    """funçao pra criar uma experincia profissional

    Args:
        request (HttpRequest): a requisição Http.(GET OU POST)
        candidate_id (int): id do candidato

    Returns:
        HttpResponse: Redireciona a pagian inicial ou
        reenderiza um template HTML com o formulario a ser preenchido
    """
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == "POST":
        form = ProfessionalExperienceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"/recruitment/candidato/{candidate.id}/curriculo")
    else:
        form = ProfessionalExperienceForm()
    return render(
        request,
        "recruitiment/professional_experience_create.html",
        {"form": form, "candidate": candidate},
    )


@login_required(login_url="user_login")
@user_passes_test(staff_required)
def professional_experience_list(
    request: HttpRequest, candidate_id: int
) -> HttpResponse:
    """Lista todos as experiencias profisionais de um candidato

    Args:
        request (HttpRequest): a requisição Http.(GET OU POST)
        candidate_id (int): id do candidato

    Returns:
        HttpResponse: mostra todas as experiencias do candidato
    """
    candidate = get_object_or_404(Candidate, id=candidate_id)
    experiences = get_list_or_404(ProfessionalExperience, candidate=candidate)
    return render(
        request,
        "recruitiment/professional_experience_list.html",
        {"candidate": candidate, "professional_experiences": experiences},
    )


# Education_views
@login_required(login_url="user_login")
def education_detail(
    request: HttpRequest, candidate_id: int, education_id: int
) -> HttpResponse:
    """Função para visualizar detalhes da Formação Educacional
        de um candidato.

    Args:
        request (HttpRequest): a requisição Http.(GET OU POST)
        candidate_id (int): O ID do candidato.
        professional_id (int): O ID da Escolaridade do candidato

    Returns:
        HttpResponse: Redireciona a pagian inicial ou
        reenderiza o template com os detalhes da
        experiência profissional.
    """
    candidate = get_object_or_404(Candidate, id=candidate_id)
    education = get_object_or_404(Education, id=education_id, candidate=candidate)
    if request.method == "POST":
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect(f"/recruitment/candidato/{candidate.id}/curriculo")
    else:
        form = EducationForm(instance=education)

    return render(
        request,
        "recruitiment/education_detail.html",
        {
            "form": form,
            "candidate": candidate,
            "education": education,
        },
    )


@login_required(login_url="user_login")
def education_create(request: HttpRequest, candidate_id: int) -> HttpResponse:
    """Função pra criar uma Formação Educacional

    Args:
        request (HttpRequest): a requisição Http.(GET OU POST)
        candidate_id (int): id do candidato

    Returns:
        HttpResponse: Redireciona a pagian inicial ou
        reenderiza um template HTML com o formulario a ser preenchido
    """
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"/recruitment/candidato/{candidate.id}/curriculo")
    else:
        form = EducationForm()
    return render(
        request,
        "recruitiment/education_create.html",
        {"form": form, "candidate": candidate},
    )


@login_required(login_url="user_login")
@user_passes_test(staff_required)
def education_list(request: HttpRequest, candidate_id: int) -> HttpResponse:
    """Lista todos as formaçoes Educacionais do Candidadto

    Args:
        request (HttpRequest): a requisição Http.(GET OU POST)
        candidate_id (int): id do candidato

    Returns:
        HttpResponse: mostra todas as experiencias do candidato
    """

    candidate = get_object_or_404(Candidate, id=candidate_id)
    educations = get_list_or_404(Education, candidate=candidate)
    return render(
        request,
        "recruitiment/education_list.html",
        {"candidate": candidate, "educations": educations},
    )


# Curriculo Completo


@login_required(login_url="user_login")
def curriculum(request: HttpRequest, candidate_id: int) -> HttpResponse:
    candidate = get_object_or_404(Candidate, id=candidate_id)
    educations = Education.objects.filter(candidate=candidate)
    experiences = ProfessionalExperience.objects.filter(candidate=candidate)
    return render(
        request,
        "recruitiment/curriculum.html",
        {"candidate": candidate, "educations": educations, "experiences": experiences},
    )
