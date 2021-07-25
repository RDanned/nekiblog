import random
from django import forms
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *
# Create your views here.


class MainPage(ListView):
    model = Post
    template_name = 'main.html'

    def get_queryset(self):
        posts = Post.objects.all()
        random_posts = random.sample(list(posts), 5)

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
        context['is_subscribed'] = UserSubscription.objects.filter(
            user=self.request.user,
            author=kwargs['pk']).exists()

        return context


class CreatePost(CreateView):
    template_name = 'post_form.html'
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return HttpResponseRedirect(reverse('profile'))

    def get_success_url(self):
        return '/profile/'


def subscribe(request, pk):
    subscription = UserSubscription(user=request.user, author_id=pk)
    subscription.save()
    return HttpResponseRedirect(reverse('user', kwargs={'pk': pk}))

def unsubscribe(request, pk):
    subscription = UserSubscription.objects.get(user=request.user, author_id=pk)
    subscription.delete()
    return HttpResponseRedirect(reverse('user', kwargs={'pk': pk}))
