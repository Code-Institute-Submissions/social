from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('<slug:slug>/', views.PostView.as_view(), name='post_detail'),
    path('deletepost/<slug:slug>/', views.DeletePost.as_view(), name='delete_post'),
    path('deletecomment/<slug:slug>/<int:comment_id>', views.DeleteComment.as_view(), name='delete_comment'),
]
