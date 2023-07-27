from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView

from blogs.models import BlogModel
from books.forms import AddReviewForm
from books.models import BookModel, CategoryModel, ReviewModel
from users.models import UserModel
from utils.utils import GetMixin


class MainView(ListView):
    model = BlogModel
    template_name = 'books/index.html'
    context_object_name = 'blogs'
    extra_context = {
        'title': 'Simpy - главная страница'
    }

    def get_queryset(self):
        blogs = BlogModel.objects.all()

        if len(blogs) > 1:
            return blogs[0], blogs[1]


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
        active_category = CategoryModel.objects.get(slug=self.kwargs["category"])
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
        context['title'] = 'Simpy - читатели'
        context['readers'] = context['book'].usermodel_set.all()
        return context


class BookReviewsView(FormView, DetailView):
    model = BookModel
    template_name = 'books/reviews.html'
    context_object_name = 'book'
    slug_url_kwarg = 'book_slug'
    form_class = AddReviewForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookReviewsView, self).get_context_data(object_list=None, **kwargs)
        context['title'] = 'Simpy - отзывы'
        context['reviews'] = context['book'].reviewmodel_set.all()
        context['flag'] = 'reviews'
        return context

    def get_success_url(self):
        return reverse_lazy('reviews', args=(self.kwargs['book_slug'],))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.book = BookModel.objects.get(slug=self.kwargs['book_slug'])
        self.object.user = self.request.user
        self.object.save()
        return super(BookReviewsView, self).form_valid(form)