from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from .models import *
# Create your views here.


class MainPage(ListView):
    model = Post
    template_name = 'main.html'

    def get_queryset(self):
        posts = Post.objects.all()[:5]

        return posts


class PostDetail(DetailView):

    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProfilePage(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    login_url = '/login/'

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


class MySubscriptionsPage(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'my_subscriptions.html'
    login_url = '/login/'

    def get_queryset(self):
        subscriptions = UserSubscription.objects.filter(user=self.request.user)

        subscribed_users = []
        for subscription in subscriptions:
            subscribed_users.append(subscription.author)

        posts = Post.objects.filter(author__in=subscribed_users).order_by('-created_at')

        return posts


def subscribe(request, pk):
    subscription = UserSubscription(user=request.user, author_id=pk)
    subscription.save()
    return HttpResponseRedirect(reverse('user', kwargs={'pk': pk}))


def unsubscribe(request, pk):
    subscription = UserSubscription.objects.get(user=request.user, author_id=pk)
    subscription.delete()
    return HttpResponseRedirect(reverse('user', kwargs={'pk': pk}))


@csrf_exempt
def view_post(request, pk):
    response = {'success': False}

    post = Post.objects.get(pk=pk)
    view = PostAction(post=post, user=request.user, viewed=True)
    view.save()

    response['success'] = True

    return JsonResponse(response, safe=False)


@csrf_exempt
def unview_post(request, pk):
    response = {'success': False}

    PostAction.objects.filter(post_id=pk, user=request.user, viewed=True).delete()

    response['success'] = True

    return JsonResponse(response, safe=False)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('main'))
