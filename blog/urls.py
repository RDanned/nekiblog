from django.urls import path

from . import views

app_name = 'applications'
urlpatterns = [
    path('main/', views.MainPage.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post.detail'),
]