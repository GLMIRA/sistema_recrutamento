from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpRequest
from django.template import loader
from .models import Candidate, ProfessionalExperience, Education
from .forms import CandidateForm


def index(request):
    return HttpResponse("index")


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
