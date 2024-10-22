from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Candidate, ProfessionalExperience, Education


def index(request):
    return HttpResponse("index")


def candidate(request, candidate_id):
    candidate = Candidate.objects.get(pk=candidate_id)
    template = loader.get_template("recrutiment/candidate_detail.html")
    context = {"candidate": candidate}
    return HttpResponse(template.render(context, request))
