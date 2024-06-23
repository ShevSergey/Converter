import telebot
import os

print("Бот запущен и работает!")

TOKEN = '7493817602:AAH3v5NCH9LXxDzOZAj645wyZ3l2PZV_IQQ'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Указываем путь для сохранения файла
        save_directory = r'C:\Users\Sergey\Desktop\Python\Convertor\downloads'
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        src = os.path.join(save_directory, message.document.file_name)
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Пожалуй, я сохраню это")
    except Exception as e:
        bot.reply_to(message, str(e))

@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    bot.reply_to(message, f'Вы написали: {message.text}')

bot.polling()
