from django.core.mail import send_mail
from django.db.models import Q, Sum
from django.shortcuts import redirect

from books.models import BookModel
from bot.bot import bot
from bot.models import BotChatModel
from msg.models import MsgModel
from simpy.settings import EMAIL_HOST_USER


MODEL = {
    'ReviewModel': 'ваш отзыв',
    'QuoteModel': 'вашу цитату',
    'BlogModel': 'ваш блог',
}


class GetMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            messages = MsgModel.objects.filter(recipient=self.request.user, is_read=False)
            context['user_books'] = self.request.user.book.all()
            context['count_messages'] = len(messages)

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
        if 'category_slug' in self.kwargs:
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

            user_object = object_name.user
            model_object_name = MODEL[self.model.__name__]
            chat_user = BotChatModel.objects.filter(user=user_object)

            if chat_user and chat_user[0].user.is_send_notifications and user != user_object:
                chat_id = chat_user[0].chat_id
                bot.send_message(chat_id, f'На {model_object_name} "{object_name}" пользователем {user} '
                                          f'оставлен новый комментарий:\n\n'
                                          f'{comment}')

            return super(CommentMixin, self).post(request, *args, **kwargs)


class LikeMixin:
    def get(self, request, *args, **kwargs):
        if 'like' in request.GET and request.user.is_authenticated:
            user = request.user
            object_name = self.model.objects.get(pk=request.GET['like'])
            like = object_name.likes.filter(user=user)

            if not like or not like[0].is_like:
                user_object = object_name.user
                model_object_name = MODEL[self.model.__name__]
                chat_user = BotChatModel.objects.filter(user=user_object)

                if chat_user and chat_user[0].user.is_send_notifications and user != user_object:
                    chat_id = chat_user[0].chat_id
                    bot.send_message(chat_id, f'Пользователь {user} оценил {model_object_name} "{object_name}"')

            if like:
                if like[0].is_like:
                    like[0].is_like = False
                else:
                    like[0].is_like = True

                like[0].save()

            else:
                object_name.likes.create(user=user, is_like=True)

        elif 'like' in request.GET and not request.user.is_authenticated:
            return redirect('login')

        return super(LikeMixin, self).get(request, *args, **kwargs)


class SortedMixin:
    def get_queryset(self):
        if 'date' in self.request.GET:
            if self.request.GET['date'] == 'up':
                return self.model.objects.order_by('create_date')

        if 'rating' in self.request.GET:
            if self.request.GET['rating'] == 'up':
                return self.model.objects.annotate(sum=Sum('likes')).order_by('sum')
            else:
                return self.model.objects.annotate(sum=Sum('likes')).order_by('-sum')

        return self.model.objects.order_by('-create_date')


def send_message(title, message, email_to):
    send_mail(
        title,
        message,
        EMAIL_HOST_USER,
        [email_to]
    )