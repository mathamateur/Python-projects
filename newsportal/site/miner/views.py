from django.shortcuts import render
from django.http import HttpResponse

from miner.models import News


def index(request):
    news = News.objects.all()
    return render(request, 'index.html', {'news': news})
