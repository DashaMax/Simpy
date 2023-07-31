from django.db.models import Q
from django.shortcuts import redirect

from books.models import BookModel


class GetMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['user_books'] = self.request.user.book.all()

        return context

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if 'delete' in request.GET:
                book_delete = BookModel.objects.get(slug=request.GET['delete'])
                self.request.user.book.remove(book_delete)

            elif 'add' in request.GET:
                book_delete = BookModel.objects.get(slug=request.GET['add'])
                self.request.user.book.add(book_delete)

        elif 'add' in request.GET:
            return redirect('login')

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        #if 'category' in self.kwargs:
        if 'category_slug' in self.kwargs:
            #obj = BookModel.objects.filter(category__slug=self.kwargs['category'])
            obj = BookModel.objects.filter(category__slug=self.kwargs['category_slug'])
        else:
            obj = super().get_queryset()

        if 'search' in self.request.GET:
            search = self.request.GET['search']
            books_search = obj.filter(Q(title__contains=search) |
                                      Q(author__name__contains=search))

            if books_search:
                return books_search

        return obj


class CommentMixin:
    def post(self, request, *args, **kwargs):
        if 'comment' in request.POST:
            user = request.user
            object_name = self.model.objects.get(pk=request.POST['pk'])
            comment = request.POST['comment']
            object_name.comments.create(user=user, comment=comment)
            return super(CommentMixin, self).post(request, *args, **kwargs)
