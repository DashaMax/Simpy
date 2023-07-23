from django.views.generic import TemplateView, ListView, DetailView

from books.models import BookModel, CategoryModel
from utils.utils import GetMixin


class MainView(TemplateView):
    template_name = 'books/index.html'
    extra_context = {
        'title': 'Simpy - главная страница'
    }


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

