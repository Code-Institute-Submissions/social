from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Post, Category, Comment
from .forms import CommentForm, PostForm


@method_decorator(login_required, name='post')
class Home(View):

    def get(self, request):
        posts = Post.objects.order_by('-post_date')
        categories = Category.objects.order_by('title')

        paginator = Paginator(posts, 5)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'index.html', {
            'page_obj': page_obj,
            'post_form': PostForm,
            'categories': categories,
        })

    def post(self, request):
        posts = Post.objects.order_by('-post_date')
        categories = Category.objects.order_by('title')

        paginator = Paginator(posts, 5)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        post_form = PostForm(request.POST, request.FILES)

        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.slug = '-'.join(post.title.split())
            post.save()
        else:
            post_form = PostForm()

        return render(request, 'index.html', {
            'page_obj': page_obj,
            'post_form': PostForm,
            'categories': categories,
        })

@method_decorator(login_required, name='post')
class PostView(View):

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        comments = post.comments.order_by('-comment_date')

        return render(request, 'post_view.html', {
            'post': post,
            'comments': comments,
            'comment_form': CommentForm()
        })

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        comments = post.comments.order_by('-comment_date')

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.author = request.user
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(request, 'post_view.html', {
            'post': post,
            'comments': comments,
            'comment_form': CommentForm()
        })


class DeletePost(View):

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        return render(request, 'delete_post.html', {
            'post': post,
        })
    
    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        post.delete()
        
        return redirect('home')
    

class DeleteComment(View):

    def get(self, request, slug, comment_id):
        post = Post.objects.get(slug=slug)
        
        return render(request, 'delete_comment.html', {
            'post': post,
            'comment_id': comment_id,
        })
    
    def post(self, request, slug, comment_id):
        com = Comment.objects.get(id=comment_id)
        com.delete()
        
        return redirect('post_detail', slug=slug)