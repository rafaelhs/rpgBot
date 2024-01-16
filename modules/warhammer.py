from telegram import *
from telegram.ext import *
import secrets
import tables.admech as admech
from .misc import restricted

@restricted
async def vox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    index = secrets.choice(range(0, 109))
    quote = '_' + admech.quotes[index][1] + '_'
    frm = '*' + admech.quotes[index][0] + '*'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=quote + "\n" + frm, parse_mode='MarkdownV2')