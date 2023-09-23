from django.core.management import BaseCommand

from bot.bot import bot
from bot.messages import (ADD_CHAT_FOR_USER_MESSAGE, ALREADY_KNOWN_MESSAGE,
                          ERROR_MESSAGE, NOT_FOUND_MESSAGE,
                          OTHER_LOGIN_MESSAGE, START_EXIST_CHAT_MESSAGE,
                          START_MESSAGE)
from bot.models import BotChatModel
from users.models import UserModel


class Command(BaseCommand):
    help = 'Starting telegram-bot SimpyBot'

    def handle(self, *args, **options):
        @bot.message_handler(commands=['start', 'help'])
        def message_start(message):
            chat_id = message.chat.id
            chat = BotChatModel.objects.filter(chat_id=chat_id)

            if chat:
                bot.send_message(message.chat.id, START_EXIST_CHAT_MESSAGE)

            else:
                bot.send_message(message.chat.id, START_MESSAGE)

        @bot.message_handler(content_types=['text'])
        def message_login(message):
            login = message.text
            user = UserModel.objects.filter(username=login)

            if user:
                user_chat = BotChatModel.objects.filter(user=user[0])
                chat_id = message.chat.id

                if not user_chat:
                    chat = BotChatModel.objects.filter(chat_id=chat_id)

                    if chat:
                        bot.send_message(
                            message.chat.id,
                            f'{OTHER_LOGIN_MESSAGE} {chat[0].user.first_name}.\n'
                            f'{ERROR_MESSAGE}'
                        )

                    else:
                        chat = BotChatModel(user=user[0], chat_id=chat_id)
                        chat.save()
                        bot.send_message(message.chat.id, ADD_CHAT_FOR_USER_MESSAGE)

                elif user_chat[0].chat_id == chat_id:
                    bot.send_message(message.chat.id, ALREADY_KNOWN_MESSAGE)

            else:
                bot.send_message(message.chat.id, NOT_FOUND_MESSAGE)

        bot.infinity_polling()