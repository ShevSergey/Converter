import telebot
import os
from docx2pdf import convert

print("Бот запущен и работает!")

TOKEN = '7493817602:AAH3v5NCH9LXxDzOZAj645wyZ3l2PZV_IQQ'
bot = telebot.TeleBot(TOKEN)

def file_convert_docx_pdf(file_path):
    # Создаем директорию для PDF файлов, если она не существует
    convert_dir = os.path.join(os.path.dirname(file_path), 'convert_pdf')
    if not os.path.exists(convert_dir):
        os.makedirs(convert_dir)

    # Формируем путь для сохранения PDF файла
    pdf_file_path = os.path.join(convert_dir, os.path.basename(file_path).replace('.docx', '.pdf'))

    # Конвертируем файл
    convert(file_path, pdf_file_path)

    return pdf_file_path

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

        # Проверка и конвертация файла, если это .docx
        if src.endswith('.docx'):
            pdf_file_path = file_convert_docx_pdf(src)
            if os.path.exists(pdf_file_path):
                with open(pdf_file_path, 'rb') as pdf_file:
                    bot.send_document(chat_id, pdf_file)
            else:
                bot.reply_to(message, "Не удалось конвертировать файл в PDF.")
        else:
            bot.reply_to(message, "Пожалуй, я сохраню это")

    except Exception as e:
        bot.reply_to(message, str(e))

@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    bot.reply_to(message, f'Вы написали: {message.text}')

bot.polling()
