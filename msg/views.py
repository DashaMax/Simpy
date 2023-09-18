from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView, DetailView

from bot.bot import bot
from bot.models import BotChatModel
from msg.forms import MessageForm
from msg.models import ChatModel
from users.models import UserModel
from utils.utils import GetMixin


class ChatsView(GetMixin, LoginRequiredMixin, ListView):
    model = ChatModel
    template_name = 'msg/chats.html'
    context_object_name = 'chats'
    extra_context = {
        'title': 'Simpy - чаты'
    }

    def get_queryset(self):
        return ChatModel.objects.filter(members__in=[self.request.user]).order_by('-last_message__date_time')


class GetChatView(GetMixin, LoginRequiredMixin, View):
    model = ChatModel
    slug_url_kwarg = 'user_slug'

    def get(self, request, user_slug):
        user1 = request.user
        user2 = get_object_or_404(UserModel, slug=user_slug)
        chat = ChatModel.objects.filter(members__in=[user1, user2]).annotate(c=Count('members')).filter(c=2)

        if not chat:
            chat = ChatModel.objects.create()
            chat.members.add(user1)
            chat.members.add(user2)
            chat_pk = chat.pk

        else:
            chat_pk = chat[0].pk

        return redirect('chat-messages', chat_pk=chat_pk)


class ChatMessagesView(GetMixin, LoginRequiredMixin, DetailView, FormView):
    model = ChatModel
    template_name = 'msg/messages.html'
    context_object_name = 'chat'
    pk_url_kwarg = 'chat_pk'
    form_class = MessageForm

    def get_context_data(self, **kwargs):
        chat = get_object_or_404(ChatModel, pk=self.kwargs['chat_pk'])
        user1 = chat.members.first()
        user2 = chat.members.last()
        member_chat = user1 if user2 == self.request.user else user2
        context = super(ChatMessagesView, self).get_context_data(**kwargs)
        context['title'] = 'Simpy - сообщения'
        context['member'] = member_chat
        context['messages'] = chat.msgmodel_set.all()
        return context

    def get(self, request, *args, **kwargs):
        chat = get_object_or_404(ChatModel, pk=self.kwargs['chat_pk'])
        user1 = chat.members.first()
        user2 = chat.members.last()

        if self.request.user in (user1, user2):
            messages = chat.msgmodel_set.filter(recipient=self.request.user)
            last_message = chat.msgmodel_set.last()
            chat.last_message = last_message
            chat.save()

            for message in messages:
                message.is_read = True
                message.save()

            return super(ChatMessagesView, self).get(request, *args, **kwargs)

        else:
            return redirect('index')

    def get_success_url(self):
        return reverse_lazy('chat-messages', args=(self.kwargs['chat_pk'],))

    def form_valid(self, form):
        chat = get_object_or_404(ChatModel, pk=self.kwargs['chat_pk'])
        user1 = chat.members.first()
        user2 = chat.members.last()
        member_chat = user1 if user2 == self.request.user else user2

        self.object = form.save(commit=False)
        self.object.chat = chat
        self.object.sender = self.request.user
        self.object.recipient = member_chat
        self.object.save()

        chat_user = BotChatModel.objects.filter(user=member_chat)

        if chat_user and chat_user[0].user.is_send_notifications:
            chat_id = chat_user[0].chat_id
            bot.send_message(chat_id, f'Привет)\n'
                                      f'Пользователь --- {self.request.user} ---\n'
                                      f'прислал новое сообщение:\n\n'
                                      f'{self.object.message}\n\n'
                                      f'Для просмотра перейдите по ссылке:\n'
                                      f'http://127.0.0.1:8000/chats/messages/{chat.pk}/')

        return super(ChatMessagesView, self).form_valid(form)