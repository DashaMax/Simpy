from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, FormView

from blogs.models import BlogModel
from users.forms import UserLoginForm, UserRegisterForm, UserUpdateForm, AddBlogForm
from users.models import UserModel
from utils.utils import GetMixin


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Simpy - авторизация'
    }

    def get_success_url(self):
        return reverse_lazy('user', args=(self.request.user.slug,))


class UserRegisterView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_message = 'Регистрация прошла успешно'
    success_url = reverse_lazy('login')
    extra_context = {
        'title': 'Simpy - регистрация'
    }


class UserView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'users/account.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['user'] = UserModel.objects.get(slug=self.kwargs['slug'])
        context['title'] = f'Simpy - {context["user"]}'
        return context


class UserEditView(LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = UserUpdateForm
    template_name = 'users/edit.html'
    extra_context = {
        'title': 'Simpy - редактирование профиля'
    }

    def get_success_url(self):
        return reverse_lazy('user', args=(self.request.user.slug,))

    def get(self, request, *args, **kwargs):
        if kwargs['slug'] != self.request.user.slug:
            return redirect('index')
        return super(UserEditView, self).get(request, *args, **kwargs)


class UserBookshelfView(GetMixin, LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'users/bookshelf.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserBookshelfView, self).get_context_data(object_list=None, **kwargs)
        context['title'] = 'Simpy - книжная полка'
        context['user'] = UserModel.objects.get(slug=self.kwargs['slug'])
        context['books'] = context['user'].book.all()
        return context


class UserBlogsView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = BlogModel
    template_name = 'users/profile-blog.html'
    form_class = AddBlogForm
    success_message = 'Статья успешно добавлена'

    def get_context_data(self, **kwargs):
        context = super(UserBlogsView, self).get_context_data(**kwargs)
        user = UserModel.objects.get(slug=self.kwargs['slug'])
        context['title'] = 'Simpy - блог'
        context['flag'] = 'user_blogs'
        context['user'] = UserModel.objects.get(slug=self.kwargs['slug'])
        context['user_blogs'] = BlogModel.objects.filter(author=user)
        return context

    def get_success_url(self):
        return reverse_lazy('user-blogs', args=(self.kwargs['slug'],))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super(UserBlogsView, self).form_valid(form)