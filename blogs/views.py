from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

from blogs.models import BlogModel
from comments.forms import AddCommentForm
from utils.utils import CommentMixin, LikeMixin, SortedMixin, GetMixin


class BlogsView(GetMixin, SortedMixin, LikeMixin, ListView):
    paginate_by = 4
    model = BlogModel
    template_name = 'blogs/blogs.html'
    context_object_name = 'blogs'
    extra_context = {
        'title': 'Simpy - блог'
    }


class BlogView(GetMixin, LikeMixin, CommentMixin, FormView, DetailView):
    model = BlogModel
    template_name = 'blogs/blog.html'
    context_object_name = 'blog'
    slug_url_kwarg = 'blog_slug'
    form_class = AddCommentForm

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        context['title'] = f'Simpy - {context["blog"]}'
        context['flag'] = 'blog'
        return context

    def get_success_url(self):
        return reverse_lazy('blog', args=(self.kwargs['blog_slug'],))

    def get(self, request, *args, **kwargs):
        if 'delete' in request.GET:
            blog = BlogModel.objects.get(pk=request.GET['delete'])

            if self.request.user == blog.user:
                blog.delete()
                return redirect('blogs')

        return super(BlogView, self).get(request, *args, **kwargs)