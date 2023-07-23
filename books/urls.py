from django.urls import path
from .views import MainView, BooksView, BooksCategoryView, BookView, BookReadersView


urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('books/', BooksView.as_view(), name='books'),
    path('books/<str:category>/', BooksCategoryView.as_view(), name='books_category'),
    path('book/<slug:book_slug>/', BookView.as_view(), name='book'),
    path('book/<slug:book_slug>/readers/', BookReadersView.as_view(), name='readers'),
]