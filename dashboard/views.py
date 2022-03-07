from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.


def dashboard_view(request: HttpRequest):
    return render(request, "index.html")

def add_trs_view(request: HttpRequest):
    return render(request, "add_training_session.html")