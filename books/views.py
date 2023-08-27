from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

from blogs.models import BlogModel
from books.forms import AddReviewForm
from books.models import BookModel, CategoryModel, ReviewModel
from bot.bot import bot
from bot.models import BotChatModel
from comments.forms import AddCommentForm
from feedback.forms import FeedbackForm
from feedback.models import FeedbackModel
from quotes.forms import AddQuoteForm
from quotes.models import QuoteModel
from simpy.settings import TITLE, MESSAGE, EMAIL_HOST_USER
from utils.utils import GetMixin, CommentMixin, send_message, LikeMixin


def error_404_view(request, exception):
    return render(request, 'books/404.html')


class MainView(GetMixin, LikeMixin, FormView):
    form_class = FeedbackForm
    template_name = 'books/index.html'
    success_url = reverse_lazy('index')
    model = BlogModel

    def get_context_data(self, **kwargs):
        blogs = BlogModel.objects.all()
        context = super(MainView, self).get_context_data(**kwargs)
        context['title'] = 'Simpy - главная страница'
        context['blogs'] = [blogs[0], blogs[1]] if len(blogs) > 1 else None
        return context

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        feedbacks = FeedbackModel.objects.first()
        pk = feedbacks.pk + 1 if feedbacks else 1
        feedback = FeedbackModel(title=request.POST['title'], email=email, feedback=request.POST['feedback'])
        feedback.save()
        title = 'Simpy - новое сообщение'
        message = f'Новое сообщение >>>\n\nТема обращения: {request.POST["title"]}\nПочта для связи: {email}\n\nПрочитать сообщение ' \
                  f'целиком можно по ссылке:\nhttp://127.0.0.1:8000/admin/feedback/feedbackmodel/{pk}/change/'
        send_message(TITLE, MESSAGE, email)
        send_message(title, message, EMAIL_HOST_USER)
        return super(MainView, self).post(request, *args, **kwargs)


class BooksView(GetMixin, ListView):
    model = BookModel
    template_name = 'books/books.html'
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        context = super(BooksView, self).get_context_data(**kwargs)
        context['title'] = 'Simpy - книги'
        context['categories'] = CategoryModel.objects.all()
        return context


class BooksCategoryView(GetMixin, ListView):
    model = BookModel
    template_name = 'books/books.html'
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        context = super(BooksCategoryView, self).get_context_data(**kwargs)
        active_category = CategoryModel.objects.get(slug=self.kwargs["category_slug"])
        context['title'] = f'Simpy - {active_category}'
        context['categories'] = CategoryModel.objects.all()
        context['active'] = active_category
        return context


class BookView(GetMixin, DetailView):
    model = BookModel
    template_name = 'books/book.html'
    context_object_name = 'book'
    slug_url_kwarg = 'book_slug'

    def get_context_data(self, **kwargs):
        context = super(BookView, self).get_context_data(**kwargs)
        context['title'] = f'Simpy - {context["book"]}'
        context['flag'] = 'book'
        return context


class BookReadersView(GetMixin, DetailView):
    model = BookModel
    context_object_name = 'book'
    template_name = 'books/readers.html'
    slug_url_kwarg = 'book_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookReadersView, self).get_context_data(object_list=None, **kwargs)
        context['title'] = f'Simpy - {context["book"]}'
        context['readers'] = context['book'].usermodel_set.all()
        return context


class BookReviewsView(GetMixin, CommentMixin, FormView, ListView):
    model = ReviewModel
    template_name = 'books/reviews.html'
    context_object_name = 'reviews'
    form_class = AddCommentForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookReviewsView, self).get_context_data(object_list=None, **kwargs)
        context['book'] = BookModel.objects.get(slug=self.kwargs['book_slug'])
        context['title'] = f'Simpy - {context["book"]}'
        context['flag'] = 'reviews'
        context['form_add_review'] = AddReviewForm
        return context

    def get_queryset(self):
        return BookModel.objects.get(slug=self.kwargs['book_slug']).reviewmodel_set.all().order_by('-create_date')

    def get_success_url(self):
        return reverse_lazy('reviews', args=(self.kwargs['book_slug'],))

    def post(self, request, *args, **kwargs):
        if 'review' in request.POST:
            form = AddCommentForm()
            book = BookModel.objects.get(slug=self.kwargs['book_slug'])
            user = request.user
            review = ReviewModel(book=book, user=user, review=request.POST['review'])
            review.save()

            book_users = book.usermodel_set.all()

            for book_user in book_users:
                chat_user = BotChatModel.objects.filter(user=book_user)

                if chat_user and chat_user[0].user.is_send_notifications and user != book_user:
                    chat_id = chat_user[0].chat_id
                    bot.send_message(chat_id, f'На книгу --- {book} ---\n'
                                              f'пользователем --- {user.first_name} ---\n'
                                              f'оставлен новый отзыв:\n\n'
                                              f'{review.review}\n\n'
                                              f'Для просмотра перейдите по ссылке:\n'
                                              f'http://127.0.0.1:8000/book/{book.slug}/reviews/')

            return super(BookReviewsView, self).form_valid(form)

        return super(BookReviewsView, self).post(request, *args, **kwargs)


class BookQuotesView(GetMixin, LikeMixin, CommentMixin, FormView, ListView):
    model = QuoteModel
    context_object_name = 'quotes'
    template_name = 'books/book-quotes.html'
    form_class = AddCommentForm

    def get_queryset(self):
        book = BookModel.objects.get(slug=self.kwargs['book_slug'])
        return QuoteModel.objects.filter(book=book).order_by('-create_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookQuotesView, self).get_context_data(object_list=None, **kwargs)
        book = BookModel.objects.get(slug=self.kwargs['book_slug'])
        context['book'] = book
        context['title'] = f'Simpy - {context["book"]}'
        context['flag'] = 'quotes'
        context['form_add_quote'] = AddQuoteForm
        return context

    def get_success_url(self):
        return reverse_lazy('book-quotes', args=(self.kwargs['book_slug'],))

    def post(self, request, *args, **kwargs):
        if 'quote' in request.POST:
            form = AddCommentForm()
            book = BookModel.objects.get(slug=self.kwargs['book_slug'])
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

            return super(BookQuotesView, self).form_valid(form)

        return super(BookQuotesView, self).post(request, *args, **kwargs)