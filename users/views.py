from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from users.forms import UserLoginForm, UserRegisterForm
from users.models import UserModel


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Simpy - авторизация'
    }

    def get_success_url(self):
        return reverse_lazy('user')


class UserRegisterView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_message = 'Регистрация прошла успешно'
    success_url = reverse_lazy('login')
    extra_context = {
        'title': 'Simpy - регистрация'
    }


class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'users/account.html'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['user'] = UserModel.objects.get(pk=self.request.user.id)
        context['title'] = f'Simpy - {context["user"]}'
        return context
