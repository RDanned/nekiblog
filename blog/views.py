import random
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import *
# Create your views here.


class MainPage(ListView):
    model = Post
    template_name = 'main.html'

    def get_queryset(self):
        posts = Post.objects.all()
        random_posts = random.sample(list(posts), 2)

        return random_posts


class PostDetail(DetailView):

    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context