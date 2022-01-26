from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponseNotFound
from django.contrib import messages
from .models import Post, Category, Comment
from .forms import CommentForm, PostForm


@method_decorator(login_required, name='post')
class Home(View):
    """
    Render 'post add' modal & post feed to users.
    """

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

            messages.add_message(request, messages.SUCCESS,
                                 'Post added successfully!')
        else:
            post_form = PostForm()

            messages.add_message(
                request, messages.WARNING, 'Something went wrong, please ' +
                'review your post and try again.')

        return render(request, 'index.html', {
            'page_obj': page_obj,
            'post_form': PostForm,
            'categories': categories,
        })


@method_decorator(login_required, name='post')
class PostView(View):
    """
    Render full post view to user & allow viewing and editing of comments.
    """

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

            messages.add_message(request, messages.SUCCESS, 'Comment added!')
        else:
            comment_form = CommentForm()

            messages.add_message(request, messages.WARNING,
                                 'Something went wrong, please try again.')

        return render(request, 'post_view.html', {
            'post': post,
            'comments': comments,
            'comment_form': CommentForm()
        })


class DeletePost(View):
    """
    Delete selected post after asking for user confirmation.
    """

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        if request.user == post.author:
            return render(request, 'delete_post.html', {
                'post': post,
            })
        else:
            return HttpResponseNotFound('<h1>Page not found.</h1>')

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)

        if request.user == post.author:
            post.delete()

            messages.add_message(request, messages.SUCCESS, 'Post deleted!')

            return redirect('home')
        else:
            return HttpResponseNotFound('<h1>Page not found.</h1>')


class DeleteComment(View):
    """
    Delete selected comment after asking for user confirmation.
    """

    def get(self, request, slug, comment_id):
        post = Post.objects.get(slug=slug)

        if request.user == post.author:
            return render(request, 'delete_comment.html', {
                'post': post,
                'comment_id': comment_id,
            })
        else:
            return HttpResponseNotFound('<h1>Page not found.</h1>')

    def post(self, request, slug, comment_id):
        post = Post.objects.get(slug=slug)

        if request.user == post.author:
            com = Comment.objects.get(id=comment_id)
            com.delete()

            messages.add_message(request, messages.SUCCESS, 'Comment deleted!')

            return redirect('post_detail', slug=slug)
        else:
            return HttpResponseNotFound('<h1>Page not found.</h1>')


class EditPost(View):
    """
    Edit selected post after asking for user confirmation.
    """

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        if request.user == post.author:
            post_form = PostForm(instance=post)

            return render(request, 'edit_post.html', {
                'post': post,
                'post_form': post_form,
            })
        else:
            return HttpResponseNotFound('<h1>Page not found.</h1>')

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)

        if request.user == post.author:
            post_form = PostForm(request.POST, request.FILES, instance=post)

            if post_form.is_valid():
                post_new = post_form.save(commit=False)
                post_new.author = request.user
                post_new.slug = '-'.join(post_new.title.split())
                post_new.save()

                messages.add_message(
                    request, messages.SUCCESS, 'Post updated!')

                return redirect('post_detail', slug=post_new.slug)
            else:
                post_form = PostForm()
                messages.add_message(
                    request, messages.WARNING, 'Something went wrong, please' +
                    ' review your post and try again.')

            return render(request, 'edit_post.html', {
                'post': post,
                'post_form': post_form,
            })
        else:
            return HttpResponseNotFound('<h1>Page not found.</h1>')


class EditComment(View):
    """
    Edit selected comment after asking for user confirmation.
    """

    def get(self, request, slug, comment_id):
        post = Post.objects.get(slug=slug)

        if request.user == post.author:
            comment = Comment.objects.get(id=comment_id)
            comment_form = CommentForm(instance=comment)

            return render(request, 'edit_comment.html', {
                'post': post,
                'comment_form': comment_form,
            })
        else:
            return HttpResponseNotFound('<h1>Page not found.</h1>')

    def post(self, request, slug, comment_id):
        post = Post.objects.get(slug=slug)

        if request.user == post.author:
            comment = Comment.objects.get(id=comment_id)
            comment_form = CommentForm(request.POST, instance=comment)
            comment_form.save()

            messages.add_message(request, messages.SUCCESS, 'Comment updated!')

            return redirect('post_detail', slug=slug)
        else:
            return HttpResponseNotFound('<h1>Page not found.</h1>')
