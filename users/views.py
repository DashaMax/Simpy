from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, FormView

from blogs.models import BlogModel
from books.models import BookModel
from bot.management.commands import bot
from bot.models import BotChatModel
from comments.forms import AddCommentForm
from quotes.forms import UserAddQuoteForm
from quotes.models import QuoteModel
from users.forms import UserLoginForm, UserRegisterForm, UserUpdateForm, AddBlogForm, UserPasswordResetForm, \
    UserSetPasswordForm
from users.models import UserModel
from utils.utils import GetMixin, CommentMixin, LikeMixin


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


class UserPasswordResetView(PasswordResetView):
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    form_class = UserPasswordResetForm
    template_name = 'users/password_reset_form.html'
    extra_context = {
        'title': 'Simpy - восстановление пароля'
    }


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'
    extra_context = {
        'title': 'Simpy - восстановление пароля'
    }


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    extra_context = {
        'title': 'Simpy - восстановление пароля'
    }


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
    extra_context = {
        'title': 'Simpy - восстановление пароля'
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
        context['title'] = f'Simpy - {context["user"]} - книжная полка'
        context['books'] = context['user'].book.all()
        return context


class UserBlogsView(LikeMixin, SuccessMessageMixin, LoginRequiredMixin, CreateView):
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
        context['user_blogs'] = BlogModel.objects.filter(user=user)
        return context

    def get_success_url(self):
        return reverse_lazy('user-blogs', args=(self.kwargs['user_slug'],))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(UserBlogsView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if 'delete' in request.GET:
            blog = BlogModel.objects.get(pk=request.GET['delete'])

            if self.request.user == blog.user:
                blog.delete()

        return super(UserBlogsView, self).get(request, *args, **kwargs)


class UserQuotesView(LikeMixin, CommentMixin, LoginRequiredMixin, FormView, ListView):
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

    def get(self, request, *args, **kwargs):
        if 'delete' in request.GET:
            quote = QuoteModel.objects.get(pk=request.GET['delete'])

            if self.request.user == quote.user:
                quote.delete()

        return super(UserQuotesView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'quote' in request.POST:
            form = AddCommentForm()
            book = BookModel.objects.get(pk=request.POST['book'])
            user = request.user
            quote = QuoteModel(book=book, user=user, quote=request.POST['quote'])
            quote.save()

            book_users = book.usermodel_set.all()

            for book_user in book_users:
                chat_user = BotChatModel.objects.filter(user=book_user)

                if chat_user and user != book_user:
                    chat_id = chat_user[0].chat_id
                    bot.bot.send_message(chat_id, f'На книгу --- {book} ---\n'
                                              f'пользователем --- {user.first_name} ---\n'
                                              f'оставлена новая цитата:\n\n'
                                              f'<< {quote.quote} >>\n\n'
                                              f'Для просмотра перейдите по ссылке:\n'
                                              f'http://127.0.0.1:8000/book/{book.slug}/quotes/')

            return super(UserQuotesView, self).form_valid(form)

        return super(UserQuotesView, self).post(request, *args, **kwargs)