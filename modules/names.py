from telegram import *
from telegram.ext import *
import secrets
import re
import tables.spanishXVI as spanishNames
from .misc import restricted

@restricted
async def getSpanishNames(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pattern = re.compile("(f|female|feminino|mulher)")
    try:
        table = 0 if pattern.match(context.args[0].lower()) else 1
    except:
        table = 1

    if table == 0:
        name = spanishNames.female[secrets.choice(range(0, len(spanishNames.female)))]
    else:
        name = spanishNames.male[secrets.choice(range(0, len(spanishNames.male)))]
    byName = spanishNames.byname[secrets.choice(range(0, len(spanishNames.byname)))]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=name + " " + byName, parse_mode='MarkdownV2')
    