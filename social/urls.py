from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('<slug:slug>/', views.PostView.as_view(), name='post_detail'),
    path('deletepost/<slug:slug>/', login_required(views.DeletePost.as_view()), name='delete_post'),
    path('deletecomment/<slug:slug>/<int:comment_id>', login_required(views.DeleteComment.as_view()), name='delete_comment'),
]
