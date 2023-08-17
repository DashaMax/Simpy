from django.urls import reverse_lazy
from django.views.generic import ListView, FormView

from comments.forms import AddCommentForm
from quotes.models import QuoteModel
from utils.utils import CommentMixin, LikeMixin, SortedMixin


class QuotesView(SortedMixin, LikeMixin, CommentMixin, FormView, ListView):
    model = QuoteModel
    context_object_name = 'quotes'
    template_name = 'quotes/quotes.html'
    extra_context = {
        'title': 'Simpy - цитаты'
    }
    form_class = AddCommentForm

    def get_success_url(self):
        return reverse_lazy('quotes')