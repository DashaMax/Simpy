from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from blogs.models import BlogModel
from books.models import BookModel
from bot.bot import bot
from bot.models import BotChatModel
from comments.forms import AddCommentForm
from quotes.forms import UserAddQuoteForm
from quotes.models import QuoteModel
from users.forms import UserLoginForm, UserRegisterForm, UserUpdateForm, AddBlogForm, UserPasswordResetForm, \
    UserSetPasswordForm
from users.models import UserModel
from utils.utils import GetMixin, CommentMixin, LikeMixin, PostMixin


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Simpy - авторизация'
    }

    def get_success_url(self):
        return reverse_lazy('user', args=(self.request.user.slug,))

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        
        return super(UserLoginView, self).get(request, *args, **kwargs)


class UserRegisterView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_message = 'Регистрация прошла успешно'
    success_url = reverse_lazy('login')
    extra_context = {
        'title': 'Simpy - регистрация'
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        return super(UserRegisterView, self).get(request, *args, **kwargs)


class UserPasswordResetView(PasswordResetView):
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    form_class = UserPasswordResetForm
    template_name = 'users/password_reset_form.html'
    extra_context = {
        'title': 'Simpy - восстановление пароля'
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        return super(UserPasswordResetView, self).get(request, *args, **kwargs)


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'
    extra_context = {
        'title': 'Simpy - восстановление пароля'
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        return super(UserPasswordResetDoneView, self).get(request, *args, **kwargs)


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

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        return super(UserPasswordResetCompleteView, self).get(request, *args, **kwargs)


class UserView(GetMixin, LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'users/account.html'
    slug_url_kwarg = 'user_slug'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['user'] = get_object_or_404(UserModel, slug=self.kwargs['user_slug'])
        context['title'] = f'Simpy - {context["user"]}'
        return context


class UserEditView(GetMixin, LoginRequiredMixin, UpdateView):
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


class UserBookshelfView(GetMixin, PostMixin, LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'users/bookshelf.html'
    context_object_name = 'user'
    slug_url_kwarg = 'user_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserBookshelfView, self).get_context_data(object_list=None, **kwargs)
        context['title'] = f'Simpy - {context["user"]} - книжная полка'
        context['books'] = context['user'].book.all()
        return context


class UserBlogsView(GetMixin, LikeMixin, LoginRequiredMixin, CreateView):
    model = BlogModel
    template_name = 'users/profile-blog.html'
    form_class = AddBlogForm

    def get_context_data(self, **kwargs):
        context = super(UserBlogsView, self).get_context_data(**kwargs)
        user = get_object_or_404(UserModel, slug=self.kwargs['user_slug'])
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

    def post(self, request, *args, **kwargs):
        if 'delete-blog' in request.POST:
            blog = get_object_or_404(BlogModel, pk=request.POST['delete-blog'])

            if self.request.user == blog.user:
                blog.delete()

        return super(UserBlogsView, self).post(request, *args, **kwargs)


class UserQuotesView(GetMixin, LikeMixin, CommentMixin, LoginRequiredMixin, ListView):
    model = QuoteModel
    template_name = 'users/profile-quotes.html'

    def get_context_data(self, **kwargs):
        context = super(UserQuotesView, self).get_context_data(**kwargs)
        user = get_object_or_404(UserModel, slug=self.kwargs['user_slug'])
        context['flag'] = 'user_quotes'
        context['user'] = UserModel.objects.get(slug=self.kwargs['user_slug'])
        context['title'] = f'Simpy - {context["user"]} - цитаты'
        context['quotes'] = QuoteModel.objects.filter(user=user).order_by('-create_date')
        context['form_add_quote'] = UserAddQuoteForm
        context['form'] = AddCommentForm
        return context

    def get_success_url(self):
        return reverse_lazy('user-quotes', args=(self.kwargs['user_slug'],))

    def post(self, request, *args, **kwargs):
        if 'quote' in request.POST:
            book = get_object_or_404(BookModel, pk=request.POST['book'])
            user = request.user
            quote = QuoteModel(book=book, user=user, quote=request.POST['quote'])
            quote.save()

            book_users = book.usermodel_set.all()

            for book_user in book_users:
                chat_user = BotChatModel.objects.filter(user=book_user)

                if chat_user and chat_user[0].user.is_send_notifications and user != book_user:
                    chat_id = chat_user[0].chat_id
                    bot.send_message(chat_id, f'На книгу --- {book} ---\n'
                                              f'пользователем --- {user.first_name} ---\n'
                                              f'оставлена новая цитата:\n\n'
                                              f'❝ {quote.quote} ❞\n\n'
                                              f'Для просмотра перейдите по ссылке:\n'
                                              f'http://127.0.0.1:8000/book/{book.slug}/quotes/')

        elif 'delete-quote' in request.POST:
            quote = get_object_or_404(QuoteModel, pk=request.POST['delete-quote'])

            if self.request.user == quote.user:
                quote.delete()

        return super(UserQuotesView, self).post(request, *args, **kwargs)