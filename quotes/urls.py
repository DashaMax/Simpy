from django.urls import path
from quotes.views import QuotesView


urlpatterns = [
    path('quotes/',  QuotesView.as_view(), name='quotes'),
]