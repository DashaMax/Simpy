from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from comments.forms import AddCommentForm
from quotes.models import QuoteModel
from utils.utils import CommentMixin, GetMixin, LikeMixin, SortedMixin


class QuotesView(GetMixin, SortedMixin, LikeMixin, CommentMixin, FormView, ListView):
    paginate_by = 4
    model = QuoteModel
    context_object_name = 'quotes'
    template_name = 'quotes/quotes.html'
    extra_context = {
        'title': 'Simpy - цитаты'
    }
    form_class = AddCommentForm

    def get_success_url(self):
        return reverse_lazy('quotes')