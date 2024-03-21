from django.shortcuts import render
from api.models import *
from api.views import *


def home(request):
    return render(request, 'index.html')