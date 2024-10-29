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
                login(request, user)
                return redirect("index", username=username)
            else:
                form.add_error(None, "usuario ou senha invalidos")
    else:
        form = LoginForm()

    return render(request, "recruitiment/user_login.html", {"form": form})


@login_required(login_url="user_login")
def index(request: HttpRequest, username: str):
    user = User.objects.get(username=username)
    candidate = Candidate.objects.filter(id=user).first()
    if request.method == "POST":
        if candidate is None:
            return redirect(f"/recruitment/candidato/criar")
        else:
            return redirect(f"/recruitment/candidato/{username}/curriculo")
    return render(
        request,
        "recruitiment/index_template.html",
        {"username": username},
    )


# ________________________Candidatos________________________ #


@login_required(login_url="user_login")
def candidate_detail(request: HttpRequest, username: str) -> HttpResponse:
    """funaço para editar candiadto

    Args:
        request (HttpRequest): tipo requisiçao(POST,GET)
        candidate_id (int): id candidato

    Returns:
        HttpResponse: Redireciona para a página inicial após salvar ou
        renderiza o template com o formulário preenchido para edição.
    """
    user = get_object_or_404(User, username=username)
    candidate = get_object_or_404(Candidate, id=user)
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
            print("estou salvando")
            candidate = form.save(commit=False)
            candidate.id = request.user
            candidate.save()
            print(candidate)
            return redirect(f"/recruitment/candidato/{candidate.id}/curriculo")
        else:
            print("nao salvei")
            print(form.errors)
    else:
        print(request.user)
        form = CandidateForm()
    return render(request, "recruitiment/candidate_create.html", {"form": form})


@login_required(login_url="user_login")
@user_passes_test(staff_required)
def candidate_list(request: HttpRequest, username: str) -> HttpResponse:
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


# ________________________Parte Profisional________________________ #


@login_required(login_url="user_login")
def professional_experience_detail(
    request: HttpRequest, candidate_username: str, experience_id: int
):
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
    user = get_object_or_404(User, username=candidate_username)
    candidate = get_object_or_404(Candidate, id=user)
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
    request: HttpRequest, candidate_username: str
) -> HttpResponse:
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
            return redirect(f"/recruitment/candidato/{candidate.id}/curriculo")
    else:
        form = ProfessionalExperienceForm()
    return render(
        request,
        "recruitiment/professional_experience_create.html",
        {"form": form, "candidate": candidate},
    )


# TODO: matar todas as views de lista
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


# ________________________Education_views________________________#


@login_required(login_url="user_login")
def education_detail(
    request: HttpRequest, candidate_username: str, education_id: int
) -> HttpResponse:
    """Recebe um nome de usuario e o id da escolaridade para edição

    Args:
        request (HttpRequest): get ou post
        username (str): Nome do Usuario
        education_id (int): id das escolaridades

    Returns:
        HttpResponse: leva o formulario ou redireciona para o curriculo
    """
    user = get_object_or_404(User, username=candidate_username)
    candidate = get_object_or_404(Candidate, id=user)
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
def education_create(request: HttpRequest, candidate_username: str) -> HttpResponse:
    """cria uma formaçao academica do Candidato

    Args:
        request (HttpRequest): (POST,GET)
        candidate_username (str): ID do candidato

    Returns:
        HttpResponse: Retorna um formulario para adicionar uma formaçao
        redireciona para a pagina do curriculo
    """
    user = get_object_or_404(User, username=candidate_username)
    candidate = get_object_or_404(Candidate, id=user.id)
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


# ________________________Curriculo Completo________________________#


@login_required(login_url="user_login")
def curriculum(request: HttpRequest, candidate_username: str) -> HttpResponse:
    user = get_object_or_404(User, username=candidate_username)
    candidate = get_object_or_404(Candidate, id=user)
    educations = Education.objects.filter(candidate=candidate)
    experiences = ProfessionalExperience.objects.filter(candidate=candidate)
    return render(
        request,
        "recruitiment/curriculum.html",
        {
            "candidate": candidate,
            "educations": educations,
            "experiences": experiences,
            "user": user,
        },
    )
