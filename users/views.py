from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, FormView

from blogs.models import BlogModel
from books.models import BookModel
from comments.forms import AddCommentForm
from quotes.forms import UserAddQuoteForm
from quotes.models import QuoteModel
from users.forms import UserLoginForm, UserRegisterForm, UserUpdateForm, AddBlogForm
from users.models import UserModel
from utils.utils import GetMixin, CommentMixin


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
    slug_url_kwarg = 'user_slug'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['user'] = UserModel.objects.get(slug=self.kwargs['user_slug'])
        context['title'] = f'Simpy - {context["user"]}'
        return context


class UserEditView(LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = UserUpdateForm
    template_name = 'users/edit.html'
    slug_url_kwarg = 'user_slug'
    extra_context = {
        'title': 'Simpy - редактирование профиля'
    }

    def get_success_url(self):
        return reverse_lazy('user', args=(self.request.user.slug,))

    def get(self, request, *args, **kwargs):
        if kwargs['user_slug'] != self.request.user.slug:
            return redirect('index')
        return super(UserEditView, self).get(request, *args, **kwargs)


class UserBookshelfView(GetMixin, LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'users/bookshelf.html'
    context_object_name = 'user'
    slug_url_kwarg = 'user_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserBookshelfView, self).get_context_data(object_list=None, **kwargs)
        #context['user'] = UserModel.objects.get(slug=self.kwargs['slug'])
        context['title'] = f'Simpy - {context["user"]} - книжная полка'
        context['books'] = context['user'].book.all()
        return context


class UserBlogsView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = BlogModel
    template_name = 'users/profile-blog.html'
    form_class = AddBlogForm
    success_message = 'Статья успешно добавлена'

    def get_context_data(self, **kwargs):
        context = super(UserBlogsView, self).get_context_data(**kwargs)
        user = UserModel.objects.get(slug=self.kwargs['user_slug'])
        context['flag'] = 'user_blogs'
        context['user'] = user
        context['title'] = f'Simpy - {context["user"]} - блог'
        context['user_blogs'] = BlogModel.objects.filter(author=user)
        return context

    def get_success_url(self):
        return reverse_lazy('user-blogs', args=(self.kwargs['user_slug'],))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super(UserBlogsView, self).form_valid(form)


class UserQuotesView(CommentMixin, LoginRequiredMixin, FormView, ListView):
    model = QuoteModel
    template_name = 'users/profile-quotes.html'
    form_class = AddCommentForm

    def get_context_data(self, **kwargs):
        context = super(UserQuotesView, self).get_context_data(**kwargs)
        user = UserModel.objects.get(slug=self.kwargs['user_slug'])
        context['flag'] = 'user_quotes'
        context['user'] = UserModel.objects.get(slug=self.kwargs['user_slug'])
        context['title'] = f'Simpy - {context["user"]} - цитаты'
        context['quotes'] = QuoteModel.objects.filter(user=user).order_by('-create_date')
        context['form_add_quote'] = UserAddQuoteForm
        return context

    def get_success_url(self):
        return reverse_lazy('user-quotes', args=(self.kwargs['user_slug'],))

    def post(self, request, *args, **kwargs):
    #     if 'comment' in request.POST:
    #         user = request.user
    #         quote = QuoteModel.objects.get(pk=request.POST['pk'])
    #         comment = request.POST['comment']
    #         quote.comments.create(user=user, comment=comment)
    #         return super(UserQuotesView, self).post(request, *args, **kwargs)
    #
        if 'text' in request.POST:
            form = AddCommentForm()
            book = BookModel.objects.get(pk=request.POST['book'])
            user = request.user
            quote = QuoteModel(book=book, user=user, text=request.POST['text'])
            quote.save()
            return super(UserQuotesView, self).form_valid(form)

        return super(UserQuotesView, self).post(request, *args, **kwargs)