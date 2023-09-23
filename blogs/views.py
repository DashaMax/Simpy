from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView

from blogs.models import BlogModel
from comments.forms import AddCommentForm
from utils.utils import CommentMixin, GetMixin, LikeMixin, SortedMixin


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

    def post(self, request, *args, **kwargs):
        if 'delete-blog' in request.POST:
            blog = get_object_or_404(BlogModel, pk=request.POST['delete-blog'])

            if self.request.user == blog.user:
                blog.delete()
                return redirect('blogs')

        return super(BlogView, self).post(request, *args, **kwargs)
