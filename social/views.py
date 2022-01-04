from django.shortcuts import render
from django.views import View
from .models import Post

class Home(View):

    def get(self, request):
        posts = Post.objects.order_by("-post_date")

        return render(request, 'index.html', {
            'posts': posts,
            'home_page': 'active'
        })
