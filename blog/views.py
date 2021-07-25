import random
from django import forms
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
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


class ProfilePage(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['subscribes'] = UserSubscription.objects.filter(user=self.request.user)
        context['posts'] = Post.objects.filter(author=self.request.user)

        return context


class UserPage(TemplateView):
    template_name = 'user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = User.objects.get(pk=kwargs['pk'])
        context['posts'] = Post.objects.filter(author=kwargs['pk'])
        context['subscribes'] = UserSubscription.objects.filter(user=kwargs['pk'])

        return context
