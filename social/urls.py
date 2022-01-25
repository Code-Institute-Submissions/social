from unicodedata import name
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('<slug:slug>/', views.PostView.as_view(), name='post_detail'),
    path('deletepost/<slug:slug>/', login_required(views.DeletePost.as_view()), name='delete_post'),
    path('deletecomment/<slug:slug>/<int:comment_id>/', login_required(views.DeleteComment.as_view()), name='delete_comment'),
    path('editpost/<slug:slug>/', login_required(views.EditPost.as_view()), name='edit_post'),
    path('editcomment/<slug:slug>/<int:comment_id>/', login_required(views.EditComment.as_view()), name='edit_comment'),
]
