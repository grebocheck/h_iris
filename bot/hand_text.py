from bot import bot

# обробка текстових команд
@bot.message_handler(content_types=['text'])
def texter(message):
    pass