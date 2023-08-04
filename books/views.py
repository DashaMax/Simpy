from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

from blogs.models import BlogModel
from books.forms import AddReviewForm, FeedbackForm
from books.models import BookModel, CategoryModel, ReviewModel
from comments.forms import AddCommentForm
from quotes.forms import AddQuoteForm
from quotes.models import QuoteModel
from utils.utils import GetMixin, CommentMixin, send_message


def error_404_view(request, exception):
    return render(request, 'books/404.html')


class MainView(FormView, ListView):
    model = BlogModel
    form_class = FeedbackForm
    template_name = 'books/index.html'
    context_object_name = 'blogs'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Simpy - главная страница'
    }

    def get_queryset(self):
        blogs = BlogModel.objects.all()

        if len(blogs) > 1:
            return blogs[0], blogs[1]

    def post(self, request, *args, **kwargs):
        title = request.POST['title']
        email = request.POST['email']
        message = request.POST['message']
        send_message(email)
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


class BookReviewsView(CommentMixin, FormView, ListView):
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
            return super(BookReviewsView, self).form_valid(form)

        return super(BookReviewsView, self).post(request, *args, **kwargs)


class BookQuotesView(CommentMixin, FormView, ListView):
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
            return super(BookQuotesView, self).form_valid(form)

        return super(BookQuotesView, self).post(request, *args, **kwargs)