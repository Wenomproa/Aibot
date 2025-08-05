import logging
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, Dispatcher
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

# Создаем объект Flask
app = Flask(__name__)

# Токен бота Telegram
TOKEN = "7886918651:AAEzbcErkGX8d4IeXqoPry_dVFMIgzy9mD0"
bot = Bot(token=TOKEN)

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Команда /start
def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Generate Image", callback_data='generate_image')],
        [InlineKeyboardButton("Edit Image", callback_data='edit_image')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome! Choose an option:', reply_markup=reply_markup)

# Генерация изображения с текстом
def generate_image(update: Update, context):
    query = update.callback_query
    query.answer()
    
    # Создание изображения с текстом
    img = Image.new('RGB', (500, 500), color = (255, 255, 255))
    d = ImageDraw.Draw(img)
    text = "Hello, AI!"
    d.text((10,10), text, fill=(0,0,0))
    
    # Сохранение изображения
    img_path = "/tmp/generated_image.png"
    img.save(img_path)
    
    query.edit_message_text(text="Image generated successfully!")
    bot.send_photo(chat_id=update.effective_chat.id, photo=open(img_path, 'rb'))

# Редактирование изображения с добавлением текста
def edit_image(update: Update, context):
    query = update.callback_query
    query.answer()
    
    # Создание и редактирование изображения
    img = Image.new('RGB', (500, 500), color = (255, 255, 255))
    d = ImageDraw.Draw(img)
    text = "Edited Image"
    d.text((10,10), text, fill=(0,0,0))
    
    # Сохранение отредактированного изображения
    img_path = "/tmp/edited_image.png"
    img.save(img_path)
    
    query.edit_message_text(text="Image edited successfully!")
    bot.send_photo(chat_id=update.effective_chat.id, photo=open(img_path, 'rb'))

# Функция для обработки webhook
def set_webhook():
    webhook_url = "https://your-vercel-url.vercel.app/webhook"
    bot.set_webhook(url=webhook_url)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        json_str = request.get_data().decode('UTF-8')
        update = Update.de_json(json_str, bot)
        dispatcher.process_update(update)
    return 'ok'

# Инициализация Dispatcher
dispatcher = Dispatcher(bot, None)
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CallbackQueryHandler(generate_image, pattern='generate_image'))
dispatcher.add_handler(CallbackQueryHandler(edit_image, pattern='edit_image'))

# Запуск Flask приложения
if __name__ == '__main__':
    set_webhook()  # Настройка webhook для Telegram
    app.run(host='0.0.0.0', port=5000)
