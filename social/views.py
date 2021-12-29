from django import http
from django.db.models import query
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post


def home(request):

    queryset = Post.objects.order_by('-post_date')

    return render(request, 'index.html', {
        'posts': queryset,
        'home_page': 'active',
        'test_var': True,
    })
