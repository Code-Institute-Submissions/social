from django import http
from django.db.models import query
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post


def home(request):

    return render(request, 'index.html', {
        'p': range(100),
        'home_page': 'active',
    })
