from telegram import *
from telegram.ext import *
import secrets
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
    str = f"_Rolando\.\.\._  {res}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=str, parse_mode='MarkdownV2')


def calcRoll(rolls):
    rollList = []
    sum = 0
    pattern = r"(?P<operator>[+-]?)(?P<number>\d+)(d(?P<dice_size>\d+))?"
    for roll in rolls:
        dict = re.match(pattern, roll)
        operator = -1 if dict['operator'] == '-' else 1
        number = int(dict['number'])
        if(dict['dice_size'] == None):
            sum += number * operator
            rollList.append(f"{number * operator}")
        else:
            dice_size = int(dict['dice_size'])
            for _ in range(number):
                rolled = secrets.choice(range(1, dice_size+1))
                rollList.append(f"{rolled * operator}")
                sum += rolled * operator
    return f"\(*{re.escape(str(sum))}*\)  ||\[_ {re.escape(','.join(rollList))} _\]||"  

#ayy lmao
def diceRoll(ammount, dice_size):
    sum = 0
    for _ in range(ammount):
        sum += secrets.choice(range(1, dice_size+1))
    return sum