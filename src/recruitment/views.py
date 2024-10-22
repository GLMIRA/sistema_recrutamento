from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpRequest
from django.template import loader
from .models import Candidate, ProfessionalExperience, Education
from .forms import CandidateForm, ProfessionalExperienceForm, EducationForm


def index(request):
    return HttpResponse("index")


# Parte Candidatos
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
            return redirect("/")
    else:
        form = CandidateForm(instance=candidate)
    return render(
        request,
        "recrutiment/candidate_detail.html",
        {"form": form, "candidate": candidate},
    )


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
            form.save()
            return redirect("/")
    else:
        form = CandidateForm()
    return render(request, "recrutiment/candidate_create.html", {"form": form})


def candidate_list(request: HttpRequest) -> HttpResponse:
    """Lista todos os Candidatos

    Args:
        request (HttpRequest): Requisição HTTP, (GET)

    Returns:
        HttpResponse: Lista todos candidatos cadastrados
    """
    candidates = get_list_or_404(Candidate)
    return render(
        request, "recrutiment/candidate_list.html", {"candidates": candidates}
    )


# Parte Profisional
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
            return redirect("/")
    else:
        form = ProfessionalExperienceForm(instance=professional_experience)
    return render(
        request,
        "recrutiment/professional_experience_detail.html",
        {
            "form": form,
            "professional_experience": professional_experience,
            "candidate": candidate,
        },
    )


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
            return redirect("/")
    else:
        form = ProfessionalExperienceForm()
    return render(
        request,
        "recrutiment/professional_experience_create.html",
        {"form": form, "candidate": candidate},
    )


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
        "recrutiment/professional_experience_list.html",
        {"candidate": candidate, "professional_experiences": experiences},
    )


# Education_views
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
            return redirect("/")
    else:
        form = EducationForm(instance=education)

    return render(
        request,
        "recrutiment/education_detail.html",
        {
            "form": form,
            "candidate": candidate,
            "education": education,
        },
    )


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
            return redirect("/")
    else:
        form = EducationForm()
    return render(
        request,
        "recrutiment/education_create.html",
        {"form": form, "candidate": candidate},
    )


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
        "recrutiment/education_list.html",
        {"candidate": candidate, "educations": educations},
    )
