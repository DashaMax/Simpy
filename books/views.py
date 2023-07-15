from django.views.generic import TemplateView, ListView

from books.models import BookModel, CategoryModel


class MainView(TemplateView):
    template_name = 'books/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['title'] = 'Simpy - главная страница'
        return context


class BooksView(ListView):
    model = BookModel
    template_name = 'books/books.html'
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        context = super(BooksView, self).get_context_data(**kwargs)
        context['title'] = 'Simpy - книги'
        context['categories'] = CategoryModel.objects.all()
        return context


class BooksCategoryView(ListView):
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

    def get_queryset(self):
        return BookModel.objects.filter(category__slug=self.kwargs['category'])


