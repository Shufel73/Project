import telebot
bot = telebot.TeleBot('?????????????')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(f"Your Chat ID is: {message.chat.id}")
    bot.reply_to(message, f"Got it! Your ID is: {message.chat.id}")

bot.infinity_polling()