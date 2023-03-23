from telegram import *
from telegram.ext import *
from random import randrange 
import re

async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ''.join(context.args).lower()
    patternAll = r"([+-]?\d{1,3}(d\d{1,3})?)([+-]\d{1,3}(d\d{1,3})?)*"
    patternSingle = r"([+-]?\d{1,3}(d\d{1,3})?)"
    if not re.fullmatch(patternAll, text):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Verifique a sintaxe")
        return
    l = re.findall(patternSingle, text)
    rolls = [i[0] for i in l]
    res = calcRoll(rolls)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Rolando {rolls}... [**{res}**]")


def calcRoll(rolls):
    res = 0
    pattern = r"(?P<operator>[+-]?)(?P<number>\d+)(d(?P<dice_size>\d+))?"
    for roll in rolls:
        dict = re.match(pattern, roll)
        operator = dict['operator']
        number = int(dict['number'])
        sum = 0
        if(dict['dice_size'] == None):
            sum = number
        else:
            dice_size = int(dict['dice_size'])
            for _ in range(number):
                rolled = randrange(1, dice_size)
                sum += rolled
        if operator == '-':
            res -= sum
        else:
            res += sum
    return res  