from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('<slug:slug>/', views.PostView.as_view(), name='post_detail'),
    path('<slug>:slug/', views.DeletePost.as_view(), name='delete_post')
]
