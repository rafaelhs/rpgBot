import logging
from telegram import *
from telegram.ext import *
import constants as Keys
import re
from random import randrange    

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=Keys.START_TEXT)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=Keys.HELP_TEXT)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="foda-se")

async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ''.join(context.args).lower()
    patternAll = r"([+-]?\d+(d\d+)?)+"
    patternSingle = r"([+-]?\d+(d\d+)?)"
    if not re.fullmatch(patternAll, text):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Verifique a sintaxe")
        return
    l = re.findall(patternSingle, text)
    rolls = [i[0] for i in l]
    res = calcRoll(rolls)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Rolando {rolls}... [**{res}**]")


def calcRoll(rolls):
    print("roll started")
    res = 0
    pattern = r"(?P<operator>[+-]?)(?P<number>\d+)(d(?P<dice_size>\d+))?"
    for roll in rolls:
        print(f"roll: {roll}")
        dict = re.match(pattern, roll)
        operator = dict['operator']
        number = int(dict['number'])
        print(dict.groupdict())
        print(f'op: {operator}, num: {number}, diSize: {dict["dice_size"]}')
        sum = 0
        if(dict['dice_size'] == None):
            sum = number
        else:
            dice_size = int(dict['dice_size'])
            for _ in range(number):
                rolled = randrange(1, dice_size)
                print(f"rolled: {rolled}")
                sum += rolled
        if operator == '-':
            res -= sum
        else:
            res += sum

    return res  

if __name__ == '__main__':
    application = ApplicationBuilder().token(Keys.API_KEY).build()
    
    start_handler = CommandHandler('start', start)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    help_handler = CommandHandler('help', help)
    roll_handler = CommandHandler('roll', roll)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(roll_handler)

    application.add_handler(unknown_handler) #added last

    application.run_polling()