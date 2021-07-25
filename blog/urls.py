from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'applications'
urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post.detail'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('profile/', views.ProfilePage.as_view(), name='profile'),
    path('users/<int:pk>/', views.UserPage.as_view(), name='user'),
]