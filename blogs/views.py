from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

from blogs.models import BlogModel
from comments.forms import AddCommentForm
from utils.utils import CommentMixin


class BlogsView(ListView):
    model = BlogModel
    template_name = 'blogs/blogs.html'
    context_object_name = 'blogs'
    extra_context = {
        'title': 'Simpy - блог'
    }

    def get_queryset(self):
        if 'date' in self.request.GET:
            if self.request.GET['date'] == 'up':
                return BlogModel.objects.order_by('create_date')

        return BlogModel.objects.order_by('-create_date')


class BlogView(CommentMixin, FormView, DetailView):
    model = BlogModel
    template_name = 'blogs/blog.html'
    context_object_name = 'blog'
    slug_url_kwarg = 'blog_slug'
    form_class = AddCommentForm

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        context['title'] = f'Simpy - {context["blog"]}'
        return context

    def get_success_url(self):
        return reverse_lazy('blog', args=(self.kwargs['blog_slug'],))