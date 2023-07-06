from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
from gappers.models import Gappers
from django.utils import timezone

def index(request):
     now = timezone.now()
     gappers = Gappers.objects.filter(date__date__gte=(now - timedelta(hours=24)).date())

     return render(request, "main_part/home.html", {"gappers":gappers})
