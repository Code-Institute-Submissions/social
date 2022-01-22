from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from .models import Post
from .forms import CommentForm


class Home(View):

    def get(self, request):
        posts = Post.objects.order_by("-post_date")
        paginator = Paginator(posts, 5)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'index.html', {
            'page_obj': page_obj,
        })


class PostView(View):

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        comments = post.comments.order_by('-comment_date')

        return render(request, 'post_view.html', {
            'post': post,
            'comments': comments,
            'comment_form': CommentForm()
        })
