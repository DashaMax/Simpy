from django.urls import path
from blogs.views import BlogsView, BlogView


urlpatterns = [
    path('blogs/', BlogsView.as_view(), name='blogs'),
    path('blog/<slug:blog_slug>/', BlogView.as_view(), name='blog'),
]