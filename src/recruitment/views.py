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


def user_register(request: HttpRequest):
    """Registra um Usuario

    Args:
        request (HttpRequest): GET,POST

    Returns:
         HttpResponse: Retorna um formulario vazio ou redireciona para login
    """
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
    """Faz o login do usuario

    Args:
        request (HttpRequest): GET,POST

    Returns:
        HttpResponse: Retorna um formulario vazio ou redireciona para o index da aplicação
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                form.add_error(None, "usuario ou senha invalidos")
    else:
        form = LoginForm()

    return render(request, "recruitiment/user_login.html", {"form": form})


@login_required(login_url="user_login")
def index(request: HttpRequest):
    """Index da aplicação

    Args:
        request (HttpRequest): GET,POST

    Returns:
         HttpResponse: Retorna um template, verifica se o usuario tem um candidato cadastrado
         se sim redireciona ele para seu curriculo se nao mostra uma mensagem na tela
         e pede para ele cadastrar um candidato.
    """
    candidate_exists = Candidate.objects.filter(id=request.user.id).exists()
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "view":
            if candidate_exists:
                return redirect(f"/recruitment/candidato/curriculo")
            else:
                return render(
                    request,
                    "recruitiment/index_template.html",
                    {"candidate": candidate_exists, "show_modal": True},
                )
        elif action == "create":
            return redirect("/recruitment/candidato/criar")

    return render(
        request,
        "recruitiment/index_template.html",
        {"candidate": candidate_exists, "show_modal": False},
    )


# ________________________Candidatos________________________ #


@login_required(login_url="user_login")
def candidate_detail(request: HttpRequest) -> HttpResponse:
    """funaço para editar candiadto

    Args:
        request (HttpRequest): tipo requisiçao(POST,GET)
        candidate_id (int): id candidato

    Returns:
        HttpResponse: Redireciona para a página inicial após salvar ou
        renderiza o template com o formulário preenchido para edição.
    """
    candidate = get_object_or_404(Candidate, id=request.user)
    if request.method == "POST":
        form = CandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            return redirect(f"/recruitment/candidato/curriculo")
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
            candidate = form.save(commit=False)
            candidate.id = request.user
            candidate.save()
            return redirect(f"/recruitment/candidato/curriculo")
    else:
        form = CandidateForm()
    return render(request, "recruitiment/candidate_create.html", {"form": form})


# ________________________Parte Profisional________________________ #


@login_required(login_url="user_login")
def professional_experience_detail(request: HttpRequest, experience_id: int):
    """Função para visualizar detalhes de uma experiência profissional
        de um candidato.

    Args:
        request (HttpRequest): A requisição HTTP.
        candidate_username (str): O nome de usuario do candidato.
        professional_id (int): O ID da experiência profissional.

    Returns:
        HttpResponse: Redireciona a pagian inicial ou
        reenderiza o template com os detalhes da
        experiência profissional.
    """
    candidate = get_object_or_404(Candidate, id=request.user)
    professional_experience = get_object_or_404(
        ProfessionalExperience, id=experience_id, candidate=candidate
    )
    if request.method == "POST":
        form = ProfessionalExperienceForm(
            request.POST, instance=professional_experience
        )
        if form.is_valid():
            form.save()
            return redirect(f"/recruitment/candidato/curriculo")
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
def professional_experience_create(request: HttpRequest) -> HttpResponse:
    """cria experiencias profissionais para um candidato

    Args:
        request (HttpRequest): GET ou POST
        candidate_username (str): Nome do Usario

    Returns:
        HttpResponse: Retorna um formulario vazio ou redireciona para o curriculo
    """
    candidate = get_object_or_404(Candidate, id=request.user)
    if request.method == "POST":
        form = ProfessionalExperienceForm(request.POST)
        # Recebo o formulario preenchido(porem esse formulario nao
        # nao tem o candidato)
        if form.is_valid():
            # pego as informaçoes desse formulario salvo(porem nao comitado)
            professional_experience = form.save(commit=False)
            # Adiciono o candidato dono desse formulario
            professional_experience.candidate = candidate
            # Salvo agora com o candidato correto
            professional_experience.save()
            # redireciono o usuario para a pagina do curriculo
            return redirect(f"/recruitment/candidato/curriculo")
    else:
        form = ProfessionalExperienceForm()
    return render(
        request,
        "recruitiment/professional_experience_create.html",
        {"form": form, "candidate": candidate},
    )


# ________________________Education_views________________________#


@login_required(login_url="user_login")
def education_detail(request: HttpRequest, education_id: int) -> HttpResponse:
    """Recebe um nome de usuario e o id da escolaridade para edição

    Args:
        request (HttpRequest): get ou post
        username (str): Nome do Usuario
        education_id (int): id das escolaridades

    Returns:
        HttpResponse: leva o formulario ou redireciona para o curriculo
    """
    candidate = get_object_or_404(Candidate, id=request.user)
    education = get_object_or_404(Education, id=education_id, candidate=candidate)
    if request.method == "POST":
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect(f"/recruitment/candidato/curriculo")
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
def education_create(request: HttpRequest) -> HttpResponse:
    """cria uma formaçao academica do Candidato

    Args:
        request (HttpRequest): (POST,GET)
        candidate_username (str): ID do candidato

    Returns:
        HttpResponse: Retorna um formulario para adicionar uma formaçao
        redireciona para a pagina do curriculo
    """
    candidate = get_object_or_404(Candidate, id=request.user)
    if request.method == "POST":
        # Recebo o formulario preenchido(porem esse formulario nao
        # nao tem o candidato)
        form = EducationForm(request.POST)
        if form.is_valid():
            # pego as informaçoes desse formulario salvo(porem nao comitado)
            education = form.save(commit=False)
            # Adiciono o candidato dono desse formulario
            education.candidate = candidate
            # Salvo agora com o candidato correto
            education.save()
            return redirect(f"/recruitment/candidato/curriculo")
    else:
        form = EducationForm()

    return render(
        request,
        "recruitiment/education_create.html",
        {"form": form, "candidate": candidate},
    )


# ________________________Curriculo Completo________________________#


@login_required(login_url="user_login")
def curriculum(request: HttpRequest) -> HttpResponse:
    """Mostra o curriculo

    Args:
        request (HttpRequest): GET.

    Returns:
        HttpResponse: Retorna o curriculo do candidato.
    """
    candidate = get_object_or_404(Candidate, id=request.user)
    educations = Education.objects.filter(candidate=candidate)
    experiences = ProfessionalExperience.objects.filter(candidate=candidate)
    return render(
        request,
        "recruitiment/curriculum.html",
        {
            "candidate": candidate,
            "educations": educations,
            "experiences": experiences,
        },
    )
