from telebot import TeleBot

from bot.models import BotChatModel
from simpy.settings import TELEGRAM_BOT_API_KEY
from users.models import UserModel


bot = TeleBot(TELEGRAM_BOT_API_KEY)


@bot.message_handler(commands=['start'])
def message_start(message):
    bot.send_message(
        message.chat.id,
        'Привет!\n'
        'Я буду присылать уведомления, если появится что-то новое по добавленным книгам.\n'
        'Но чтобы я точно знал, что это именно вы, пришлите мне, пожалуйста, ваш логин с книжного сервиса Simpy.'
    )


@bot.message_handler(content_types='text')
def message_login(message):
    login = message.text
    user = UserModel.objects.filter(username=login)

    if user:
        user_chat = BotChatModel.objects.filter(user=user[0])
        chat_id = message.chat.id

        if not user_chat:
            chat = BotChatModel(user=user[0], chat_id=chat_id)
            chat.save()
            user[0].is_send_notifications = True
            user[0].save()
            bot.send_message(message.chat.id,
                             'Ура! Теперь я смогу отправлять вам уведомления об обновлениях по вашим книгам :)'
            )

        elif user_chat[0].chat_id:
            bot.send_message(message.chat.id, 'А мы с вами уже знакомы :)')

        else:
            user_chat[0].chat_id = chat_id
            user_chat[0].save()
            bot.send_message(message.chat.id,
                             'Ура! Теперь я смогу отправлять вам уведомления об обновлениях по вашим книгам :)'
            )

    else:
        bot.send_message(message.chat.id,
                         'Не могу вас найти среди списка пользователей :(\n'
                         'Возможно, вы не прошли регистрацию на сервисе Simpy или неверно вводите данные.\n'
                         'Перепроверьте и попробуйте ещё раз!'
        )


bot.infinity_polling()