from django.shortcuts import render, redirect
from django.http import HttpResponse
from recruitment import views


def index(request):
    return render(request, "recruitiment/pegho_index.html")
