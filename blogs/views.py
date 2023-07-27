from django.views.generic import ListView, DetailView

from blogs.models import BlogModel


class BlogsView(ListView):
    model = BlogModel
    template_name = 'blogs/blogs.html'
    context_object_name = 'blogs'
    extra_context = {
        'title': 'Simpy - блог'
    }

    def get_queryset(self):
        return BlogModel.objects.order_by('-create_date')


class BlogView(DetailView):
    model = BlogModel
    template_name = 'blogs/blog.html'
    context_object_name = 'blog'
    slug_url_kwarg = 'blog_slug'

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        context['title'] = f'Simpy - {context["blog"]}'
        return  context