from django.urls import path
from books.views import MainView, BooksView, BooksCategoryView, BookView, BookReadersView, BookReviewsView, BookQuotesView


urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('books/', BooksView.as_view(), name='books'),
    path('books/<str:category_slug>/', BooksCategoryView.as_view(), name='books-category'),
    #path('books/<str:category>/', BooksCategoryView.as_view(), name='books_category'),
    path('book/<slug:book_slug>/', BookView.as_view(), name='book'),
    path('book/<slug:book_slug>/readers/', BookReadersView.as_view(), name='readers'),
    path('book/<slug:book_slug>/reviews/', BookReviewsView.as_view(), name='reviews'),
    path('book/<slug:book_slug>/quotes/', BookQuotesView.as_view(), name='book-quotes'),
    #path('book/<slug:book_slug>/quotes/', BookQuotesView.as_view(), name='quotes'),
]